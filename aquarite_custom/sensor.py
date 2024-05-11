"""Aquarite Sensor entities."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, BRAND, MODEL
from .aquarite_entities import SENSOR_ENTITIES

async def async_setup_entry(hass: HomeAssistant, entry, async_add_entities) -> bool:
    """Set up a config entry."""
    dataservice = hass.data[DOMAIN].get(entry.entry_id)

    if not dataservice:
        return False

    pool_id = dataservice.get_value("id")
    pool_name = dataservice.get_pool_name(pool_id)

    entities = []
    for sensor_config in SENSOR_ENTITIES:
        if "conditional_path" not in sensor_config or dataservice.get_value(sensor_config["conditional_path"]):
            entities.append(
                AquariteSensorEntity(hass, dataservice, pool_id, pool_name, sensor_config)
            )

    async_add_entities(entities)
    return True

class AquariteSensorEntity(CoordinatorEntity, SensorEntity):
    def __init__(self, hass: HomeAssistant, dataservice, pool_id, pool_name, sensor_config):
        super().__init__(dataservice)
        self._dataservice = dataservice
        self._pool_id = pool_id
        self._pool_name = pool_name
        self._config = sensor_config
        self._name = f"{pool_name}_{self._config['name']}"
        self._value_path = self._config['value_path']
        self._attr_device_class = self._config.get('device_class')
        self._attr_native_unit_of_measurement = self._config.get('unit')
        self._attr_icon = self._config.get('icon')
        self._unique_id = f"{pool_id}-{self._config['name']}"

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
    def native_value(self):
        """Return the value of the sensor."""
        value = self._dataservice.get_value(self._value_path)
        if 'conversion' in self._config:
            return self._config['conversion'](value)
        return value
