"""The nomics component."""
from __future__ import annotations

from datetime import timedelta
import json
import logging

from nomics import Nomics

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    CONF_API_KEY,
    CONF_DISPLAY_CURRENCY,
    CONF_NAME,
    CONF_QUOTE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, INVALID_API_KEY, SCAN_INTERVAL_MINUTES

PLATFORMS = ["sensor"]

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Airly as config entry."""

    api_key = entry.data[CONF_API_KEY]
    quote = str(entry.data[CONF_QUOTE]).replace(" ", "")
    display_currency = entry.data[CONF_DISPLAY_CURRENCY]
    name = entry.data[CONF_NAME]
    update_interval = timedelta(minutes=SCAN_INTERVAL_MINUTES)

    if entry.unique_id is None:
        hass.config_entries.async_update_entry(
            entry, unique_id=name
        )

    coordinator = NomicsDataUpdateCoordinator(
        hass, api_key, quote, display_currency, update_interval
    )

    entry.async_on_unload(entry.add_update_listener(update_listener))

    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN][entry.entry_id] = coordinator

    hass.config_entries.async_setup_platforms(entry, PLATFORMS)
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)

    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)

    return unload_ok

async def update_listener(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Update listener."""
    await hass.config_entries.async_reload(entry.entry_id)


class NomicsDataUpdateCoordinator(DataUpdateCoordinator):
    """Define an object to hold Nomics data."""

    def __init__(
        self,
        hass: HomeAssistant,
        api_key: str,
        quotes: str,
        display_currency: str,
        update_interval: timedelta,
    ) -> None:
        """Initialize."""
        self.hass = hass
        self._api_key = api_key
        self._quotes = quotes
        self.data = {}
        self.api = NomicsAPI(self.hass, self._api_key)
        self.display_currency = display_currency
        super().__init__(hass, _LOGGER, name=DOMAIN, update_interval=update_interval)

    
    async def _async_update_data(self) -> dict[str, str | float | int]:
        """Update data via library."""
        data = {}
        try:
            result = await self.hass.async_add_executor_job(
                self.api.get_currencies, self._quotes, self.display_currency
            )
            if result:
                if str(result).strip() == INVALID_API_KEY:
                    raise UpdateFailed("Invalid API key")

                result = json.loads(json.dumps(result, indent=4))
                quotes = self._quotes.split(",")
                for quote in quotes:
                    quote_data = [x for x in result if x["currency"] == quote.upper()]
                    if quote_data:
                        data[quote] = quote_data[0]

        except Exception as err: # pylint: disable=broad-except
            _LOGGER.warning("Unable to fetch data from Nomics: %s", err)
        return data


class NomicsAPI:
    """Get the latest data and update the states."""
    def __init__(self, hass: HomeAssistant, api_key: str) -> None:
        self.hass = hass
        self._api = Nomics(api_key)

    def get_currencies(self, ids, display_currency):
        data = self._api.Currencies.get_currencies(ids=ids, convert=display_currency, per_page=100)
        return data

    async def get_exchange_rates(self):
        data = await self.hass.async_add_executor_job(self._api.ExchangeRates.get_rates)
        return data
