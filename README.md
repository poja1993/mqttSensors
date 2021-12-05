# mqttSensors

In homeassistant, add in the configuration.yaml the following:

switch:
  - platform: mqtt
    name: "MagicMirror"
    command_topic: "mirror/request"
    state_topic: "mirror/state_topic"
    availability_topic: "mirror/availability"
