# Hayward CUSTOM AquaRite integration for Home Assistant.

# More as a place holder for now, allow users full customization of the entities retrieved / update from / to the API.
# I use it as a POC, might leverage for other integrations.

## Requirements
- An Hayward AquaRite with wifi module connected to the internet.
- The controller must be added to an Hayward account.

## Installation
Component is installed via HACS or alternative by downloading the files and placing them in your custom_components folder.

Afterwards you can go to the Integrations sections and click the add integration button. Search for Aquarite and choose to add the integration.

- First step will ask you to enter you username and password. 
- Second step will ask you to choose the pool (controller) you want to add

It will automatically add all the sensors to your Home Assistant installation.

Example dashboard, inspired from the great work of https://github.com/alexdelprete/HA-NeoPool-MQTT

![image](https://github.com/fdebrus/hayward-ha/assets/33791533/ef570ca5-d4dd-4a3d-b5c1-e1379c1d6a14)

## Customization

Entities are defined in aquarite_entities.py with their names and firestore document path. 
You can add / remove / change to your needs.

Modification will be visible as from next integration restart.
If you delete entries, make sure to clean it from the entities list to keep the integration tidy. 

```
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
```


