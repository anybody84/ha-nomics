"""Support for nomics.com exchange rates service."""
from datetime import timedelta
import logging
from typing import Any, cast

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_DISPLAY_CURRENCY, CONF_QUOTE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import NomicsDataUpdateCoordinator
from .const import (
    ATTRIBUTES,
    ATTRIBUTION,
    DEFAULT_ICON,
    DEFAULT_NAME,
    DOMAIN,
    HIST_ATTRIBUTES,
    KEY_PRICE,
    MANUFACTURER,
    MODEL,
    SCAN_INTERVAL_MINUTES,
    SPECIAL_ICONS,
)

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=SCAN_INTERVAL_MINUTES)

async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Nomics sensor entities based on a config entry."""
    initial_quotes = entry.data[CONF_QUOTE]
    display_currency = entry.data[CONF_DISPLAY_CURRENCY]
    quotes = initial_quotes.replace(" ", "").split(",")
    
    coordinator = hass.data[DOMAIN][entry.entry_id]

    sensors = [NomicsSensor(coordinator, currency=quote, display_currency=display_currency) for quote in quotes]
    async_add_entities(sensors, True)


class NomicsSensor(CoordinatorEntity, SensorEntity):
    """Representation of a Sensor."""
    coordinator: NomicsDataUpdateCoordinator

    def __init__(self, coordinator: NomicsDataUpdateCoordinator, currency: str, display_currency: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._currency = currency
        self._display_currency = display_currency
        self._attr_name = f"{DEFAULT_NAME} {self._currency}"
        self._state = None
        self._icon = DEFAULT_ICON
        self._attrs: dict[str, Any] = {ATTR_ATTRIBUTION: ATTRIBUTION}
        self._attr_unique_id = f"{DOMAIN}-{self._currency}".lower()
        
    @property
    def native_value(self) -> StateType:
        """Return the state."""
        try:
            state = self.coordinator.data[self._currency][KEY_PRICE]
            return cast(StateType, state)
        except KeyError:
            return cast(StateType, None)
        except TypeError:
            return cast(StateType, None)

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._display_currency

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        if self._currency in SPECIAL_ICONS:
            self._icon = SPECIAL_ICONS[self._currency]
        return self._icon

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        if self.coordinator.data:
            currency_data = self.coordinator.data[self._currency]
            if currency_data:
                for attr in ATTRIBUTES:
                    try:
                        self._attrs[attr] = currency_data[attr]
                    except KeyError:
                        self._attrs[attr] = None
                        _LOGGER.debug(
                            "Failed to get the attribute '%s' for %s", attr, self._currency
                        )

                for attr in HIST_ATTRIBUTES:
                    try:
                        self._attrs[f"{attr}_price_change_pct"] = round(
                            float(currency_data[attr]["price_change_pct"]) * 100, 2
                        )
                    except KeyError:
                        self._attrs[f"{attr}_price_change_pct"] = None
                        _LOGGER.debug(
                            "Failed to get the history attribute '%s' for %s",
                            attr,
                            self._currency,
                        )
        return self._attrs

    @property
    def device_info(self) -> DeviceInfo:
        """Device info."""
        return DeviceInfo(
            default_name=DEFAULT_NAME,
            entry_type="service",
            identifiers={(DOMAIN,)},  # type: ignore[arg-type]
            manufacturer=MANUFACTURER,
            model=MODEL,
        )