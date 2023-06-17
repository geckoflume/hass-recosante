import logging
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.core import callback
from .const import DOMAIN, TITLE, CONF_INSEE_CODE, CONF_CITY
from .api import INSEEAPI

_LOGGER = logging.getLogger(__name__)

ZIPCODE_SCHEMA = vol.Schema({vol.Required("zip_code", default=""): cv.string})


async def get_insee_code(hass: HomeAssistant, data: dict) -> None:
    """Get Insee code from zip code"""
    session = async_get_clientsession(hass)
    try:
        client = INSEEAPI(session)
        return await client.get_data(data)
    except ValueError as exc:
        raise exc


def _build_place_key(city) -> str:
    return f"{city['code']};{city['nom']}"


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Recosanté."""

    def __init__(self):
        """Initialize"""
        self.data = None
        self._init_info = {}
        self.city_insee = []

    @callback
    def _show_setup_form(self, step_id=None, user_input=None, schema=None, errors=None):
        """Show the setup form to the user."""

        if user_input is None:
            user_input = {}

        return self.async_show_form(
            step_id=step_id,
            data_schema=schema,
            errors=errors or {},
        )

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        return await self.async_step_location(user_input)

    async def async_step_location(self, user_input=None):
        """Handle location step"""
        errors = {}
        if user_input is not None:
            city_insee = user_input.get(CONF_INSEE_CODE)
            if not city_insee:
                # get INSEE Code
                try:
                    self.city_insee = await get_insee_code(
                        self.hass, user_input["zip_code"]
                    )
                except ValueError:
                    errors["base"] = "noinsee"
                if not errors:
                    self.data = user_input
                    return await self.async_step_multilocation()
                else:
                    return self._show_setup_form(
                        "location", user_input, ZIPCODE_SCHEMA, errors
                    )
            return self.async_create_entry(
                title=f"{TITLE} - {self.data.get(CONF_CITY)}", data=self.data
            )
        return self._show_setup_form("location", None, ZIPCODE_SCHEMA, errors)

    async def async_step_multilocation(self, user_input=None):
        """Handle location step"""
        errors = {}
        locations_for_form = {}
        for city in self.city_insee:
            locations_for_form[_build_place_key(city)] = f"{city['nom']}"

        if not user_input:
            if len(self.city_insee) > 1:
                return self.async_show_form(
                    step_id="multilocation",
                    data_schema=vol.Schema(
                        {
                            vol.Required("city", default=[]): vol.In(
                                locations_for_form
                            ),
                        }
                    ),
                    errors=errors,
                )
            user_input = {CONF_CITY: _build_place_key(self.city_insee[0])}

        city_infos = user_input[CONF_CITY].split(";")
        self.data[CONF_INSEE_CODE] = city_infos[0]
        self.data[CONF_CITY] = city_infos[1]
        return await self.async_step_location(self.data)
