""" Les constantes pour l'intégration Recosanté """
from dataclasses import dataclass
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import (
    Platform,
    UV_INDEX,
)


DOMAIN = "recosante"
COORDINATOR = "coordinator"
UNDO_LISTENER = "undo_listener"
NAME = "Recosanté"

# List of platforms to support. There should be a matching .py file for each,
# eg <cover.py> and <sensor.py>
PLATFORMS: list[Platform] = [Platform.SENSOR]
CLIENT_TIMEOUT = 10
BASE_URL = "https://api.recosante.beta.gouv.fr"
DATA_URL = f"{BASE_URL}/v1/?show_raep=true&show_indice_uv=true&insee="
API_GOUV_URL = "https://geo.api.gouv.fr/communes?"

ATTRIBUTION = "Recosanté"
MODEL = "Recosanté API"
CONF_INSEE_CODE = "INSEE"
CONF_CITY = "city"
TITLE = "Recosanté"
REFRESH_INTERVAL = 60

ICON_ALERT = "mdi:alert-decagram"
ICON_GAS = "mdi:molecule"
ICON_GRASS = "mdi:grass"
ICON_PARTICULATE = "mdi:blur"
ICON_TREE = "mdi:tree"


@dataclass
class JSONKeys:
    """Class containing required JSON keys."""

    category: str
    array: str
    label: str


@dataclass
class RecosanteRequiredKeysMixin:
    """Mixin for required keys."""

    json_keys: JSONKeys


@dataclass
class RecosanteSensorEntityDescription(
    SensorEntityDescription, RecosanteRequiredKeysMixin
):
    """Describes Recosanté sensor entity."""


ATMO_SENSORS: tuple[RecosanteSensorEntityDescription, ...] = (
    RecosanteSensorEntityDescription(
        key="no2",
        name="Dioxyde d'azote",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GAS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="indice_atmo", array="details", label="NO2"),
    ),
    RecosanteSensorEntityDescription(
        key="o3",
        name="Ozone",
        device_class=SensorDeviceClass.AQI,
        state_class=SensorStateClass.MEASUREMENT,
        icon=ICON_GAS,
        json_keys=JSONKeys(category="indice_atmo", array="details", label="O3"),
    ),
    RecosanteSensorEntityDescription(
        key="pm10",
        name="PM10",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_PARTICULATE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="indice_atmo", array="details", label="PM10"),
    ),
    RecosanteSensorEntityDescription(
        key="pm25",
        name="PM25",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_PARTICULATE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="indice_atmo", array="details", label="PM2,5"),
    ),
    RecosanteSensorEntityDescription(
        key="so2",
        name="Dioxyde de soufre",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GAS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="indice_atmo", array="details", label="SO2"),
    ),
    RecosanteSensorEntityDescription(
        key="indice_atmo",
        name="Indice ATMO de la qualité de l'air",
        icon=ICON_ALERT,
        json_keys=JSONKeys(category="indice_atmo", array=None, label=None),
    ),
)

METEO_SENSORS: tuple[RecosanteSensorEntityDescription, ...] = (
    RecosanteSensorEntityDescription(
        key="meteo",
        name="Vigilance Météo",
        device_class=SensorDeviceClass.AQI,
        icon="mdi:cloud-alert",
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="vigilance_meteo", array="details", label=None),
    ),
)

POLLUTION_SENSORS: tuple[RecosanteSensorEntityDescription, ...] = (
    RecosanteSensorEntityDescription(
        key="ep_so2",
        name="Épisode pollution dioxyde de soufre",
        icon=ICON_ALERT,
        json_keys=JSONKeys(
            category="episodes_pollution", array="details", label="Dioxyde de soufre"
        ),
    ),
    RecosanteSensorEntityDescription(
        key="ep_o3",
        name="Épisode pollution ozone",
        icon=ICON_ALERT,
        json_keys=JSONKeys(
            category="episodes_pollution", array="details", label="Ozone"
        ),
    ),
    RecosanteSensorEntityDescription(
        key="ep_no2",
        name="Épisode pollution dioxyde d'azote",
        icon=ICON_ALERT,
        json_keys=JSONKeys(
            category="episodes_pollution", array="details", label="Dioxyde d’azote"
        ),
    ),
    RecosanteSensorEntityDescription(
        key="ep_pm10",
        name="Épisode pollution PM10",
        icon=ICON_ALERT,
        json_keys=JSONKeys(
            category="episodes_pollution", array="details", label="Particules PM10"
        ),
    ),
)

RADON_SENSORS: tuple[RecosanteSensorEntityDescription, ...] = (
    RecosanteSensorEntityDescription(
        key="radon",
        name="Potentiel Radon",
        device_class=SensorDeviceClass.AQI,
        icon="mdi:radioactive",
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="potentiel_radon", array=None, label=None),
    ),
)

RAEP_SENSORS: tuple[RecosanteSensorEntityDescription, ...] = (
    RecosanteSensorEntityDescription(
        key="noisetier",
        name="Noisetier",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="noisetier"),
    ),
    RecosanteSensorEntityDescription(
        key="aulne",
        name="Aulne",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="aulne"),
    ),
    RecosanteSensorEntityDescription(
        key="peuplier",
        name="Peuplier",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="peuplier"),
    ),
    RecosanteSensorEntityDescription(
        key="saule",
        name="Saule",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="saule"),
    ),
    RecosanteSensorEntityDescription(
        key="frene",
        name="Frêne",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="frene"),
    ),
    RecosanteSensorEntityDescription(
        key="charme",
        name="Charme",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="charme"),
    ),
    RecosanteSensorEntityDescription(
        key="bouleau",
        name="Bouleau",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="bouleau"),
    ),
    RecosanteSensorEntityDescription(
        key="platane",
        name="Platane",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="platane"),
    ),
    RecosanteSensorEntityDescription(
        key="chene",
        name="Chêne",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="chene"),
    ),
    RecosanteSensorEntityDescription(
        key="olivier",
        name="Olivier",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="olivier"),
    ),
    RecosanteSensorEntityDescription(
        key="tilleul",
        name="Tilleul",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="tilleul"),
    ),
    RecosanteSensorEntityDescription(
        key="chataignier",
        name="Châtaignier",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="chataignier"),
    ),
    RecosanteSensorEntityDescription(
        key="rumex",
        name="Rumex (Oseille)",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_TREE,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="rumex"),
    ),
    RecosanteSensorEntityDescription(
        key="graminees",
        name="Graminées",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GRASS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="graminees"),
    ),
    RecosanteSensorEntityDescription(
        key="plantain",
        name="Plantain",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GRASS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="plantain"),
    ),
    RecosanteSensorEntityDescription(
        key="urticacees",
        name="Urticacées",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GRASS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="urticacees"),
    ),
    RecosanteSensorEntityDescription(
        key="armoises",
        name="Armoises",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GRASS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="armoises"),
    ),
    RecosanteSensorEntityDescription(
        key="ambroisies",
        name="Ambroisies",
        device_class=SensorDeviceClass.AQI,
        icon=ICON_GRASS,
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="raep", array="details", label="ambroisies"),
    ),
    RecosanteSensorEntityDescription(
        key="risque_allergie",
        name="Risque d'allergie aux pollens",
        icon=ICON_ALERT,
        json_keys=JSONKeys(category="raep", array=None, label=None),
    ),
)

UV_SENSORS: tuple[RecosanteSensorEntityDescription, ...] = (
    RecosanteSensorEntityDescription(
        key="uv",
        name="UV",
        native_unit_of_measurement=UV_INDEX,
        icon="mdi:sunglasses",
        state_class=SensorStateClass.MEASUREMENT,
        json_keys=JSONKeys(category="indice_uv", array=None, label=None),
    ),
)
