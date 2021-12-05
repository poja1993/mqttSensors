# mqttSensors

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
