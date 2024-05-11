"""Aquarite Light entity."""

from homeassistant.components.light import LightEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BRAND, MODEL
from .aquarite_entities import LIGHT_ENTITIES

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> bool:

    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    if not dataservice:
        return False
        
    pool_id = dataservice.get_value("id")
    pool_name = dataservice.get_pool_name(pool_id)
    
    entities = [
        AquariteLightEntity(hass, dataservice, pool_id, pool_name, light_entity["name"], light_entity["value_path"])
        for light_entity in LIGHT_ENTITIES
    ]

    async_add_entities(entities)

    return True

class AquariteLightEntity(CoordinatorEntity, LightEntity):

    def __init__(self, hass: HomeAssistant, dataservice, pool_id, pool_name, name, value_path) -> None:

        super().__init__(dataservice)
        self._dataservice = dataservice
        self._pool_id = pool_id
        self._pool_name = pool_name
        self._attr_name = f"{self._pool_name}_{name}"
        self._value_path = value_path
        self._unique_id = f"{self._pool_id}{name}"

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {(DOMAIN, self._pool_id)},
            "name": self._pool_name,
            "manufacturer": BRAND,
            "model": MODEL,
        }

    @property
    def unique_id(self):
        """The unique id of the sensor."""
        return self._unique_id

    @property
    def color_mode(self):
        return "ONOFF"

    @property
    def supported_color_modes(self):
        return {"ONOFF"}

    @property
    def is_on(self):
        """Return true if the device is on."""
        return bool(self._dataservice.get_value(self._value_path))

    async def async_turn_on(self, **kwargs):
        # Optimistically set the state to on
        self._dataservice.set_value(self._value_path, "1")
        self.async_write_ha_state()
        try:
            await self._dataservice.api.turn_on_switch(self._pool_id, self._value_path)
        except Exception as e:
            # Revert state on error
            self._dataservice.set_value(self._value_path, "0")
            self.async_write_ha_state()
            raise

    async def async_turn_off(self, **kwargs):
        # Optimistically set the state to off
        self._dataservice.set_value(self._value_path, "0")
        self.async_write_ha_state()
        try:
            await self._dataservice.api.turn_off_switch(self._pool_id, self._value_path)
        except Exception as e:
            # Revert state on error
            self._dataservice.set_value(self._value_path, "1")
            self.async_write_ha_state()
            raise