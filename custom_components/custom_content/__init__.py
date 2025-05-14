"""The Custom Markdown integration."""
from __future__ import annotations

import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, ServiceCall, callback
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.helpers.service import async_register_admin_service

from .const import DOMAIN, DEFAULT_NAME

_LOGGER = logging.getLogger(__name__)

PLATFORMS = ["sensor"]

# Service call schema for updating content - NO entity_id here
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
    
    # Get all the entities from our domain once setup is done
    all_entities = {}
    
    # Store the entity after it's created
    def store_entity(entity):
        """Store an entity for service calls."""
        all_entities[entity.entity_id] = entity
    
    # Track when entities are added
    async def async_track_entity_added(entity):
        """Track when entities are added."""
        store_entity(entity)
    
    # Add current entities
    for entry_id, entity in hass.data[DOMAIN].items():
        store_entity(entity)
    
    # Register service
    async def handle_update_content(call: ServiceCall) -> None:
        """Handle the service call to update content."""
        content = call.data["content"]
        title = call.data.get("title")
        
        # Handle entity_ids from service.target
        for entity_id in call.target.get("entity_id", []):
            if entity_id in all_entities:
                entity = all_entities[entity_id]
                await entity.async_update_content(content, title)
                _LOGGER.debug(f"Updated content for {entity_id}")
            else:
                _LOGGER.error(f"Entity {entity_id} not found")
    
    # Register admin service - this properly handles targeting
    async_register_admin_service(
        hass,
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