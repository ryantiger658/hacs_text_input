"""Sensor platform for Custom Markdown integration."""
from __future__ import annotations

from datetime import datetime
import json
from typing import Any, Optional
import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback, ServiceCall
from homeassistant.helpers.entity_platform import AddEntitiesCallback, async_get_current_platform
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

# Define the update service
SERVICE_UPDATE_CONTENT = "update_content"
SERVICE_SCHEMA = {
    vol.Required("content"): cv.string,
    vol.Optional("title"): cv.string,
}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the sensor platform."""
    _LOGGER.info("Setting up Custom Markdown platform via YAML configuration")
    # Not implementing YAML config for simplicity

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    _LOGGER.info(f"Setting up Custom Markdown sensor for entry: {config_entry.entry_id}")
    
    entity = CustomMarkdownSensor(
        config_entry.data["name"],
        config_entry.data.get("initial_title", "Content"),
        config_entry.data.get("initial_content", ""),
        config_entry.entry_id,
    )
    
    # Store the entity reference in hass.data
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][config_entry.entry_id] = entity
    
    async_add_entities([entity])
    
    # Register entity service
    platform = async_get_current_platform()
    _LOGGER.info(f"Registering entity service {SERVICE_UPDATE_CONTENT} on platform {platform}")
    
    try:
        platform.async_register_entity_service(
            SERVICE_UPDATE_CONTENT,
            SERVICE_SCHEMA,
            "async_update_content",
        )
        _LOGGER.info(f"Successfully registered entity service: {SERVICE_UPDATE_CONTENT}")
    except Exception as e:
        _LOGGER.error(f"Error registering entity service: {e}")
    
    # Add a direct entity service for testing
    async def direct_update_test(call: ServiceCall) -> None:
        """Direct update service for testing."""
        _LOGGER.error(f"DIRECT UPDATE TEST CALLED! Call data: {call.data}")
        _LOGGER.error(f"DIRECT UPDATE TEST CALLED! Call.target: {call.target if hasattr(call, 'target') else 'No target attribute'}")
        
        # Try to find the entity
        entity_id = call.data.get("entity_id")
        if entity_id:
            _LOGGER.error(f"Looking for entity: {entity_id}")
            for entry_id, stored_entity in hass.data[DOMAIN].items():
                if stored_entity.entity_id == entity_id:
                    _LOGGER.error(f"Found entity: {entity_id}")
                    content = call.data.get("content", "Test content")
                    title = call.data.get("title")
                    await stored_entity.async_update_content(content, title)
                    break
    
    # Register direct service for testing
    hass.services.async_register(
        DOMAIN,
        "direct_update_test",
        direct_update_test,
        schema=vol.Schema({
            vol.Required("entity_id"): cv.entity_id,
            vol.Required("content"): cv.string,
            vol.Optional("title"): cv.string,
        }),
    )


class CustomMarkdownSensor(SensorEntity):
    """Representation of a Custom Markdown sensor."""

    def __init__(self, name: str, initial_title: str, initial_content: str, entry_id: str) -> None:
        """Initialize the sensor."""
        self._attr_name = name
        self._title = initial_title
        self._content = initial_content
        self._last_updated = datetime.now().isoformat()
        self._entry_id = entry_id
        self._attr_unique_id = f"{DOMAIN}_{name.lower().replace(' ', '_')}"
        _LOGGER.info(f"Initialized CustomMarkdownSensor: {self._attr_name} with entity_id: {self.entity_id}")
    
    @property
    def native_value(self) -> str:
        """Return the value of the sensor."""
        return self._title

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the state attributes."""
        return {
            "content": self._content,
            "last_updated": self._last_updated,
            "title": self._title,
            "entry_id": self._entry_id,
        }
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:text-box"
    
    async def async_update_content(self, content: str, title: Optional[str] = None) -> None:
        """Update content and timestamp. This is called by the service."""
        _LOGGER.error(f"async_update_content called on {self.entity_id} with content: {content[:20]}... and title: {title}")
        
        self._content = content
        if title:
            self._title = title
        self._last_updated = datetime.now().isoformat()
        self.async_write_ha_state()
        
        _LOGGER.error(f"Content updated for {self.entity_id}")