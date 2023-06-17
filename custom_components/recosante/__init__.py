""" Les constantes pour l'intégration Recosanté """
import logging
from datetime import timedelta, date
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.typing import ConfigType
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import RecosanteDataApi
from .const import (
    DOMAIN,
    COORDINATOR,
    UNDO_LISTENER,
    PLATFORMS,
    CONF_INSEE_CODE,
    REFRESH_INTERVAL,
    NAME,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Initialisation from a config entry."""
    _LOGGER.info(
        "Initializing %s integration with plaforms: %s with config: %s",
        DOMAIN,
        PLATFORMS,
        entry,
    )
    hass.data.setdefault(DOMAIN, {})
    api = RecosanteDataApi(entry.data, hass=hass)

    coordinator = RecosanteApiCoordinator(hass=hass, config=entry, api=api)

    await coordinator.async_config_entry_first_refresh()

    # Add and update listener
    undo_listener = entry.add_update_listener(_async_update_listener)

    # Setup coordinator
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR: coordinator,
        UNDO_LISTENER: undo_listener,
    }

    await hass.config_entries.async_forward_entry_setups(entry, [Platform.SENSOR])
    _LOGGER.debug("Setup of %s successful", entry.title)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok


async def _async_update_listener(hass: HomeAssistant, entry: ConfigEntry):
    """Update when config_entry options update"""
    await hass.config_entries.async_reload(entry.entry_id)


class RecosanteApiCoordinator(DataUpdateCoordinator):
    """A coordinator to fetch data from the API only once"""

    def __init__(self, hass, config: ConfigType, api):
        super().__init__(
            hass,
            _LOGGER,
            name=NAME,  # for logging purposes
            update_method=self._update_method,
            update_interval=timedelta(minutes=REFRESH_INTERVAL),
        )
        self.config = config
        self.hass = hass
        self.api = api

    async def _update_method(self):
        data = await self.api.get_data(self.config.data[CONF_INSEE_CODE])
        if data is not None and len(data) > 0:
            return True
        else:
            self.async_set_update_error(
                f'No Data from Recosanté for INSEE code {self.config.data[CONF_INSEE_CODE]} and date {date.today().strftime("%Y-%m-%d")}'
            )
            return False

    async def async_unload_entry(self, hass: HomeAssistant, entry: ConfigEntry) -> bool:
        """This method is called to clean all sensors before re-adding them"""
        _LOGGER.debug("async_unload_entry method called")
        unload_ok = await hass.config_entries.async_unload_platforms(
            entry, [Platform.SENSOR]
        )
        if unload_ok:
            hass.data[DOMAIN].pop(entry.entry_id)
        return unload_ok
