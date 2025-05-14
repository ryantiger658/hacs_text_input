"""Sensor platform for Custom Content integration."""
from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType

from .const import DOMAIN


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    entity = CustomContentSensor(
        config_entry.data["name"],
        config_entry.data["initial_title"],
        config_entry.data["initial_content"],
    )
    
    # Store the entity reference in hass.data for the service
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    hass.data[DOMAIN][config_entry.entry_id] = entity
    
    async_add_entities([entity])


class CustomContentSensor(SensorEntity):
    """Representation of a Custom Content sensor."""

    def __init__(self, name: str, initial_title: str, initial_content: str) -> None:
        """Initialize the sensor."""
        self._attr_name = name
        self._title = initial_title
        self._content = initial_content
        self._last_updated = datetime.now().isoformat()
        self._attr_unique_id = f"{DOMAIN}_{name.lower().replace(' ', '_')}"
    
    @property
    def native_value(self) -> StateType:
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
    
    @callback
    async def async_update_content(self, content: str, title: Optional[str] = None) -> None:
        """Update content and timestamp."""
        self._content = content
        if title:
            self._title = title
        self._last_updated = datetime.now().isoformat()
        self.async_write_ha_state()