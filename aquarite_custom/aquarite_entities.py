from homeassistant.components.sensor import SensorDeviceClass
from homeassistant.const import UnitOfTemperature

from .const import PATH_HASCD, PATH_HASCL, PATH_HASPH, PATH_HASRX, PATH_HASUV, PATH_HASHIDRO

SENSOR_ENTITIES = [
    {"name": "Temperature", "value_path": "main.temperature", "device_class": SensorDeviceClass.TEMPERATURE, "unit": UnitOfTemperature.CELSIUS},
    {"name": "CD", "value_path": "modules.cd.current", "conditional_path": PATH_HASCD},
    {"name": "Cl", "value_path": "modules.cl.current", "conditional_path": PATH_HASCL, "icon": "mdi:gauge"},
    {"name": "pH", "value_path": "modules.ph.current", "device_class": SensorDeviceClass.PH, "conditional_path": PATH_HASPH},
    {"name": "Rx", "value_path": "modules.rx.current", "conditional_path": PATH_HASRX, "unit": "mV", "icon": "mdi:gauge"},
    {"name": "UV", "value_path": "modules.uv.current", "conditional_path": PATH_HASUV},
    {"name": "Electrolysis", "value_path": "hidro.current", "conditional_path": PATH_HASHIDRO, "unit": "%", "icon": "mdi:gauge"},
    {"name": "Hidrolysis Cell Time", "value_path": "hidro.cellTotalTime", "unit": "Hours", "conversion": lambda x: round(float(x) / 3600000, 2)}
]

BINARY_SENSOR_ENTITIES = [
    {"name": "Hidro Flow Status", "value_path": "hidro.fl1"},
    {"name": "Filtration Status", "value_path": "filtration.status"},
    {"name": "Backwash Status", "value_path": "backwash.status"},
    {"name": "Hidro Cover Reduction", "value_path": "hidro.cover"},
    {"name": "pH Pump Alarm", "value_path": "modules.ph.al3"},
    {"name": "CD Module Installed", "value_path": "main.hasCD"},
    {"name": "CL Module Installed", "value_path": "main.hasCL"},
    {"name": "RX Module Installed", "value_path": "main.hasRX"},
    {"name": "pH Module Installed", "value_path": "main.hasPH"},
    {"name": "IO Module Installed", "value_path": "main.hasIO"},
    {"name": "Hidro Module Installed", "value_path": "main.hasHidro"},
    {"name": "pH Acid Pump", "value_path": "modules.ph.pump_high_on"},
    {"name": "Heating Status", "value_path": "relays.filtration.heating.status"}
]

SWITCH_ENTITIES = [
    {"name": "Electrolysis Cover", "value_path": "hidro.cover_enabled"},
    {"name": "Electrolysis Boost", "value_path": "hidro.cloration_enabled"},
    {"name": "Relay1", "value_path": "relays.relay1.info.onoff"},
    {"name": "Relay2", "value_path": "relays.relay2.info.onoff"},
    {"name": "Relay3", "value_path": "relays.relay3.info.onoff"},
    {"name": "Relay4", "value_path": "relays.relay4.info.onoff"},
    {"name": "Filtration Status", "value_path": "filtration.status"}
]

LIGHT_ENTITIES = [
    {"name": "Light", "value_path": "light.status"}
]

NUMBER_ENTITIES = [
    {"name": "Redox Setpoint", "value_path": "modules.rx.status.value", "min": 500, "max": 800},
    {"name": "pH Low", "value_path": "modules.ph.status.low_value", "min": 500, "max": 800},
    {"name": "pH Max", "value_path": "modules.ph.status.high_value", "min": 500, "max": 800},
    {"name": "Hydrolysis Setpoint", "value_path": "hidro.level", "min": 0, "max_dynamic": "hidro.maxAllowedValue"}
]

SELECT_ENTITIES = [
    {"name": "Pump Mode", "value_path": "filtration.mode", "allowed_values": ["Manual", "Auto", "Heat", "Smart", "Intel"]},
    {"name": "Pump Speed", "value_path": "filtration.manVel", "allowed_values": ["Slow", "Medium", "High"]}
]


