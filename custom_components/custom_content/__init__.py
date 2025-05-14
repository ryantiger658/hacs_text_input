"""The Custom Content integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

# Service call schema for updating content
SERVICE_UPDATE_CONTENT = "update_content"
UPDATE_CONTENT_SCHEMA = vol.Schema({
    vol.Required("entity_id"): cv.entity_id,
    vol.Required("content"): cv.string,
    vol.Optional("title"): cv.string,
})

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Content from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    async def handle_update_content(call: ServiceCall) -> None:
        """Handle the service call to update content."""
        entity_id = call.data.get("entity_id")
        content = call.data.get("content")
        title = call.data.get("title")
        
        # Find the entity
        entity = None
        for entry_id, stored_entity in hass.data[DOMAIN].items():
            if stored_entity.entity_id == entity_id:
                entity = stored_entity
                break
        
        if entity:
            await entity.async_update_content(content, title)
            _LOGGER.debug(f"Updated content for {entity_id}")
        else:
            _LOGGER.error(f"Entity {entity_id} not found")
    
    # Register service
    hass.services.async_register(
        DOMAIN,
        SERVICE_UPDATE_CONTENT,
        handle_update_content,
        schema=UPDATE_CONTENT_SCHEMA,
    )
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok