""" Implements the sensors component """
import logging
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
)
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.device_registry import DeviceEntryType

from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
)
from .const import (
    DOMAIN,
    COORDINATOR,
    ATTRIBUTION,
    ATMO_SENSORS,
    METEO_SENSORS,
    POLLUTION_SENSORS,
    RADON_SENSORS,
    RAEP_SENSORS,
    UV_SENSORS,
    CONF_CITY,
    CONF_INSEE_CODE,
    MODEL,
    TITLE,
    RecosanteSensorEntityDescription,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
):
    """Configuration"""
    config = hass.data[DOMAIN][entry.entry_id]
    coordinator = config[COORDINATOR]

    entities = [
        RecosanteEntity(hass, entry, sensor_description, coordinator)
        for sensor_description in (
            ATMO_SENSORS
            + METEO_SENSORS
            + POLLUTION_SENSORS
            + RADON_SENSORS
            + RAEP_SENSORS
            + UV_SENSORS
        )
    ]
    async_add_entities(entities, True)


class RecosanteEntity(CoordinatorEntity, SensorEntity):
    """La classe de l'entité Recosanté"""

    entity_description: RecosanteSensorEntityDescription

    def __init__(
        self,
        hass: HomeAssistant,
        entry_infos,
        description: SensorEntityDescription,
        coordinator,
    ) -> None:
        """Initisalisation de l'entité"""
        super().__init__(coordinator)

        self._hass = hass
        self.entity_description = description
        self._attr_name = f"{description.name} - {entry_infos.data.get(CONF_CITY)}"
        self._attr_unique_id = f"{entry_infos.entry_id} - {entry_infos.data.get(CONF_INSEE_CODE)} - {description.name}"
        self._coordinator = coordinator
        self._attr_attribution = f"{ATTRIBUTION} - {self._coordinator.api.get_source(self.entity_description.json_keys.category)}"
        self._attr_device_class = description.device_class

        self._attr_device_info = DeviceInfo(
            name=TITLE,
            entry_type=DeviceEntryType.SERVICE,
            identifiers={
                (
                    DOMAIN,
                    f"{self._coordinator.api.get_source(self.entity_description.json_keys.category)} - {entry_infos.data.get(CONF_CITY)}",
                )
            },
            manufacturer=f"{self._coordinator.api.get_source(self.entity_description.json_keys.category)}",
            model=MODEL,
        )
        _LOGGER.debug("Creating a Recosanté sensor, named %s", self._attr_name)

    @property
    def native_value(self):
        value = self._coordinator.api.get_key(
            self.entity_description.json_keys.category,
            self.entity_description.json_keys.array,
            self.entity_description.json_keys.label,
        )
        if value is not None:
            if "value" in value:
                value = value.get("value")
            elif "level" in value:
                value = value.get("level")
            else:
                value = None
        _LOGGER.debug("Value for sensor %s is now %s", self._attr_name, value)
        return value

    @property
    def extra_state_attributes(self):
        (forecast_start, forecast_end) = self._coordinator.api.get_forecast_dates(
            self.entity_description.json_keys.category
        )
        return {
            "forecast_start": forecast_start,
            "forecast_end": forecast_end,
            "label": self._level2string(
                self._coordinator.api.get_key(
                    self.entity_description.json_keys.category,
                    self.entity_description.json_keys.array,
                    self.entity_description.json_keys.label,
                )
            ),
            "area_validity": self._coordinator.api.get_validity(
                self.entity_description.json_keys.category
            ),
        }

    def _level2string(self, value):
        return value.get("label") if value else None
