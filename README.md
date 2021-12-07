# mqttSwitch
_In Progress..._\
\
Create a Switch based on MQTT and HomeAssistant.\
The following sub-topics are used:
- availability: online/offline
- request: ON/OFF, Command request from HomeAssistant
- state_topic: ON/OFF, Feedback to command

In homeassistant, add in the configuration.yaml the following:
```yaml
switch:
  - platform: mqtt
    name: "MagicMirror"
    command_topic: "mirror/request"
    state_topic: "mirror/state_topic"
    availability_topic: "mirror/availability"
```
In this case "mirror" represents myTopic
