"""Aquarite Select entities."""
from homeassistant.components.select import SelectEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BRAND, MODEL
from .aquarite_entities import SELECT_ENTITIES

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> bool:
    """Set up a config entry."""
    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    if not dataservice:
        return False

    pool_id = dataservice.get_value("id")
    pool_name = dataservice.get_pool_name(pool_id)

    entities = [
        AquariteSelectEntity(hass, dataservice, select_entity["name"], select_entity["value_path"], pool_id, pool_name, select_entity["allowed_values"])
        for select_entity in SELECT_ENTITIES
    ]

    async_add_entities(entities)
    return True

class AquariteSelectEntity(CoordinatorEntity, SelectEntity):
    def __init__(self, hass, dataservice, name, value_path, pool_id, pool_name, allowed_values):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._pool_id = pool_id
        self._pool_name = pool_name
        self._attr_name = f"{self._pool_name}_{name}"
        self._value_path = value_path
        self._unique_id = dataservice.get_value("id") + name
        self._allowed_values = allowed_values

    @property
    def unique_id(self):
        """The unique id of the sensor."""
        return self._unique_id

    @property
    def device_info(self):
        """Return the device info."""
        return {
            "identifiers": {
                (DOMAIN, self._pool_id)
            },
            "name": self._pool_name,
            "manufacturer": BRAND,
            "model": MODEL,
        }

    @property
    def options(self) -> list[str]:
        return list(self._allowed_values)

    @property
    def current_option(self) -> str:
        return self._allowed_values[self._dataservice.get_value(self._value_path)]

    async def async_select_option(self, option: str):
        if "filtration.manVel" in self._value_path:
            """Set pump speed"""
            await self._dataservice.api.set_pump_speed(self._pool_id, self._allowed_values.index(option))
        elif "filtration.mode" in self._value_path:
            """Set pump mode"""
            await self._dataservice.api.set_pump_mode(self._pool_id, self._allowed_values.index(option))