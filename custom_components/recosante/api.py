import logging
import aiohttp
from aiohttp.client import ClientTimeout, ClientError
from homeassistant.core import HomeAssistant
from .const import DATA_URL, API_GOUV_URL

DEFAULT_TIMEOUT = 120
CLIENT_TIMEOUT = ClientTimeout(total=DEFAULT_TIMEOUT)

_LOGGER = logging.getLogger(__name__)


class RecosanteDataApi:
    """API to get Recosanté data"""

    def __init__(
        self,
        config,
        session: aiohttp.ClientSession = None,
        timeout=CLIENT_TIMEOUT,
        hass: HomeAssistant = None,
    ) -> None:
        self._timeout = timeout
        if session is not None:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()
        self._config = config
        self._data = None
        self._hass = hass

    async def get_data(self, insee_code) -> dict:
        """Get Data from Recosante API"""
        headers = {}
        url = f"{DATA_URL}{insee_code}"
        _LOGGER.debug("Getting data from %s", url)
        try:
            result = await self._session.get(url, headers=headers)
            json = await result.json()
            _LOGGER.debug("Got response %s ", json)
            _LOGGER.debug("Extracting data for INSEE %s", insee_code)
            if len(json) > 0:  # At least one result
                # Extract data for current day
                self._data = json
                _LOGGER.debug(
                    "Extracted data for INSEE %s: %s",
                    insee_code,
                    self._data,
                )
            else:  # no result
                self._data = None
                _LOGGER.warning("No data for INSEE %s", insee_code)
            return json
        except ClientError as err:
            return err

    def get_key(self, key_category, key_array, key):
        """Get value for the given key in JSON Data"""
        if self._data is not None and key_category in self._data:
            if key_array in self._data.get(key_category).get("indice"):
                for a in self._data.get(key_category).get("indice")[key_array]:
                    if a["label"] == key:
                        return a.get("indice") if "indice" in a else a
                return None
            else:
                return self._data.get(key_category).get("indice")
        else:
            return None

    def get_source(self, key_category):
        """Get value for source of data"""
        if self._data is not None and key_category in self._data:
            sources = [a["label"] for a in self._data.get(key_category).get("sources")]
            return ", ".join(sources)
        return None

    def get_forecast_dates(self, key_category):
        """Get value of data update"""
        if self._data is not None and key_category in self._data:
            dates = self._data.get(key_category).get("validity")
            return (dates.get("start"), dates.get("end")) if dates else (None, None)
        return (None, None)

    def get_validity(self, key_category):
        """Get value of validity"""
        if self._data is not None and key_category in self._data:
            if "area_details" in self._data.get(key_category).get("validity"):
                area_details = (
                    self._data.get(key_category).get("validity").get("area_details")
                )
                return f"{area_details.get('type').capitalize()} {area_details.get('charniere')}{area_details.get('nom')}"
            else:
                return self._data.get(key_category).get("validity").get("area")
        return None


class INSEEAPI:
    """API to get INSEE data"""

    def __init__(
        self, session: aiohttp.ClientSession = None, timeout=CLIENT_TIMEOUT
    ) -> None:
        self._timeout = timeout
        if session is not None:
            self._session = session
        else:
            self._session = aiohttp.ClientSession()

    async def get_data(self, zipcode) -> dict:
        """Get INSEE code for a given zip code"""
        url = f"{API_GOUV_URL}codePostal={zipcode}&fields=s=code,nom&format=json&geometry=centre"
        result = await self._session.get(url)
        if result.status == 200:
            json = await result.json()
            _LOGGER.debug("Got response for INSEE Code %s ", json)
            if len(json) == 0:
                _LOGGER.error("No INSEE value fetched for %s ", zipcode)
                raise ValueError
            return json
        else:
            _LOGGER.error("Failed to get INSEE data, with status %s ", result.status)
            raise ValueError
