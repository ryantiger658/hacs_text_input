"""The Custom Markdown integration."""
from __future__ import annotations

import logging
import voluptuous as vol
import json

from homeassistant.core import HomeAssistant, callback, ServiceCall
from homeassistant.helpers import entity_platform
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Set up the Custom Markdown component."""
    _LOGGER.info("Setting up Custom Markdown integration")
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Markdown from a config entry."""
    _LOGGER.info(f"Setting up Custom Markdown entry: {entry.entry_id}")
    hass.data.setdefault(DOMAIN, {})
    
    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Add a simple service to test if service registration works at all
    async def handle_test_service(call: ServiceCall) -> None:
        """Test service to check if service registration works."""
        _LOGGER.error(f"TEST SERVICE CALLED! Call data: {call.data}")
        _LOGGER.error(f"TEST SERVICE CALLED! Call.target: {call.target if hasattr(call, 'target') else 'No target attribute'}")
        
        # Dump the full call object for examination
        call_vars = vars(call)
        safe_call_vars = {k: str(v) for k, v in call_vars.items() if k != 'hass'}
        _LOGGER.error(f"TEST SERVICE CALLED! Call object vars: {json.dumps(safe_call_vars, indent=2)}")
    
    # Register a test service
    hass.services.async_register(
        DOMAIN,
        "test_service",
        handle_test_service,
        schema=vol.Schema({
            vol.Optional("message"): cv.string,
        }),
    )
    
    _LOGGER.info(f"Custom Markdown entry setup complete: {entry.entry_id}")
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    _LOGGER.info(f"Unloading Custom Markdown entry: {entry.entry_id}")
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok