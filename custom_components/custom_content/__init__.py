"""The Custom Markdown integration."""
from __future__ import annotations

import logging
import voluptuous as vol

from homeassistant.core import HomeAssistant, callback, ServiceCall
from homeassistant.helpers import entity_platform
from homeassistant.config_entries import ConfigEntry
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

# Define the update service
SERVICE_UPDATE_CONTENT = "update_content"
SERVICE_SCHEMA = {
    vol.Required("content"): cv.string,
    vol.Optional("title"): cv.string,
}

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Markdown from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok