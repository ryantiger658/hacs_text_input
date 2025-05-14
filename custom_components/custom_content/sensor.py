"""Sensor platform for Custom Markdown integration."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback, async_get_current_platform
import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN

# Define the update service
SERVICE_UPDATE_CONTENT = "update_content"
SERVICE_SCHEMA = {
    vol.Required("content"): cv.string,
    vol.Optional("title"): cv.string,
}

async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
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
    platform.async_register_entity_service(
        SERVICE_UPDATE_CONTENT,
        SERVICE_SCHEMA,
        "async_update_content",
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
        }
    
    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend."""
        return "mdi:text-box"
    
    async def async_update_content(self, content: str, title: Optional[str] = None) -> None:
        """Update content and timestamp. This is called by the service."""
        self._content = content
        if title:
            self._title = title
        self._last_updated = datetime.now().isoformat()
        self.async_write_ha_state()