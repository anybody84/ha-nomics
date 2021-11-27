"""Adds config flow for Nomics."""
from __future__ import annotations

import asyncio
import logging
from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import (
    CONF_API_KEY,
    CONF_DISPLAY_CURRENCY,
    CONF_NAME,
    CONF_QUOTE,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from . import NomicsAPI
from .const import DEFAULT_CURRENCY, DEFAULT_NAME, DOMAIN, INVALID_API_KEY

_LOGGER = logging.getLogger(__name__)

class NomicsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for Nomics."""

    VERSION = 1

    async def async_step_user(self, user_input = None) -> FlowResult:
        """Handle a flow initialized by the user."""
        errors = {}
        if user_input is not None:
            await self.async_set_unique_id(DEFAULT_NAME)
            self._abort_if_unique_id_configured()
            
            api_key_valid = await test_api_key(self.hass, user_input[CONF_API_KEY])
            if api_key_valid:
                return self.async_create_entry(title=DEFAULT_NAME, data={**user_input})
            else:
                errors["base"] = "invalid_api_key"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_API_KEY): str,
                    vol.Required(CONF_QUOTE, default="BTC, ETH"): str,
                    vol.Optional(CONF_DISPLAY_CURRENCY, default=DEFAULT_CURRENCY): str,
                    vol.Optional(CONF_NAME, default=DEFAULT_NAME): str,
                }
            ),
            errors = errors
        )


async def test_api_key(hass: HomeAssistant, api_key: str) -> bool:
    """Return true if api_key is valid."""
    api = NomicsAPI(hass, api_key)
    result = await api.get_exchange_rates()

    # API allows only 1 request per second.
    # This is to avoid an error while the first coordinator update
    await asyncio.sleep(2)

    if str(result).strip() == INVALID_API_KEY:
        return False
    return True