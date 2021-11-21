"""Support for nomics.com exchange rates service."""
from datetime import timedelta
import logging
import json

from nomics import Nomics
import voluptuous as vol
from typing import Any

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import (
    ATTR_ATTRIBUTION,
    CONF_API_KEY,
    CONF_NAME,
    CURRENCY_DOLLAR,
    CONF_QUOTE,
)

from .const import (
    ATTRIBUTION,
    DOMAIN,
    DEFAULT_ICON,
    SPECIAL_ICONS,
    SCAN_INTERVAL_MINUTES,
    DEFAULT_NAME,
    MANUFACTURER,
    ATTRIBUTES,
    HIST_ATTRIBUTES,
)
from homeassistant.helpers.entity import DeviceInfo
import homeassistant.helpers.config_validation as cv
from homeassistant.util import Throttle

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=SCAN_INTERVAL_MINUTES)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_API_KEY): cv.string,
        vol.Required(CONF_QUOTE): vol.All(cv.ensure_list, [cv.string]),
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    }
)


def setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the Nomics sensor."""

    api_key = config[CONF_API_KEY]
    quotes = config[CONF_QUOTE]
    api = NomicsAPI(api_key, quotes)

    sensors = [NomicsSensor(hass, api, quote) for quote in quotes]

    async_add_entities(sensors, True)


class NomicsSensor(SensorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass, api, quote):
        """Initialize the sensor."""
        self._hass = hass
        self._api = api
        self._state = None
        self._currency = quote
        self._icon = DEFAULT_ICON
        self._attrs: dict[str, Any] = {ATTR_ATTRIBUTION: ATTRIBUTION}
        self._attr_device_info = DeviceInfo(
            entry_type="service",
            identifiers={(DOMAIN, self._currency)},
            manufacturer=MANUFACTURER,
            name=DEFAULT_NAME,
        )
        self._attr_unique_id = f"{DOMAIN}-{self._currency}".lower()

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"Nomics {self._currency}"

    @property
    def state(self):
        """Return the state of the sensor."""
        currency_data = self.get_currency_data()
        if currency_data:
            return float(currency_data["price"])

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return CURRENCY_DOLLAR

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        if self._currency in SPECIAL_ICONS:
            self._icon = SPECIAL_ICONS[self._currency]
        return self._icon

    @property
    def available(self):
        """Could the device be accessed during the last update call."""
        return self._api.available

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        currency_data = self.get_currency_data()
        if currency_data:
            for attr in ATTRIBUTES:
                self._attrs[attr] = currency_data[attr]

            for attr in HIST_ATTRIBUTES:
                self._attrs[f"{attr}_price_change_pct"] = round(
                    float(currency_data[attr]["price_change_pct"]) * 100, 2
                )
        return self._attrs

    def update(self):
        """Get the latest data from Nomics."""
        self._api.update()

    def get_currency_data(self):
        """Get the data relevant for the given currency."""
        currency_data = [
            x for x in self._api.data if x["currency"] == self._currency.upper()
        ]
        if currency_data:
            return currency_data[0]
        else:
            return None


class NomicsAPI:
    """Get the latest data and update the states."""

    def __init__(self, api_key, quotes):
        self._api_key = api_key
        self._quotes = quotes
        self.data = {}
        self.available = True
        self.api = Nomics(self._api_key)
        self.update()

    @Throttle(SCAN_INTERVAL)
    def update(self):
        """Get the latest data from Nomics."""
        ids = ",".join(self._quotes)
        try:
            result = self.api.Currencies.get_currencies(ids=ids)
            if result:
                self.data = json.loads(json.dumps(result, indent=4))
                self.available = True
        except Exception:
            _LOGGER.error("Unable to fetch data from Nomics")
            self.available = False
