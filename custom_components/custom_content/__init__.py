"""The Custom Markdown integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

# Service call schema for updating content
SERVICE_UPDATE_CONTENT = "update_content"
UPDATE_CONTENT_SCHEMA = vol.Schema({
    vol.Required("content"): cv.string,
    vol.Optional("title"): cv.string,
})

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Custom Markdown from a config entry."""
    hass.data.setdefault(DOMAIN, {})
    
    # Forward the setup to the sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    
    # Register services
    @callback
    async def handle_update_content(call: ServiceCall) -> None:
        """Handle the service call to update content."""
        content = call.data.get("content")
        title = call.data.get("title")
        target_entities = await service_target_to_entities(hass, call)
        
        for entity in target_entities:
            await entity.async_update_content(content, title)
            _LOGGER.debug(f"Updated content for {entity.entity_id}")
    
    # Helper to convert target to entities
    async def service_target_to_entities(hass, call):
        """Convert service call target to a list of entities."""
        entity_registry = hass.helpers.entity_registry.async_get(hass)
        entities = []
        
        # Process entity IDs from target
        entity_ids = await hass.helpers.target.async_extract_target_entities(
            hass, call
        )
        
        for entity_id in entity_ids:
            # Find the entity in our domain
            for entry_id, stored_entity in hass.data[DOMAIN].items():
                if stored_entity.entity_id == entity_id:
                    entities.append(stored_entity)
                    break
        
        return entities
    
    # Register service with target support
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