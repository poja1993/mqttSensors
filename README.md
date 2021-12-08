# mqttSwitch
_In Progress..._\
\
Create a Switch based on MQTT and HomeAssistant.\
The following topics are used:
- myTopic/availability: online/offline
- myTopic/request: ON/OFF, Command request from HomeAssistant
- myTopic/state_topic: ON/OFF, Feedback to command

## System Requirements
Tested with python 3.7 installed on dietpi

## Installation
- clone repository in <my_path>
- Create Python VEnv: python3 -m venv <my_path>/mqttSwitch/
- cd <my_path>/mqttSwitch/
- Activate Python VEnv: source bin/activate
- Install dependencies: pip3 install -r requirements.txt
- Copy and modify template files: \
cp json.config.template json.config \
cp mqttSwitch.service.template mqttSwitch.service.template
- Copy service file: \
sudo cp mqttSwitch.service /etc/systemd/system/mqttSwitch.service
- Enable and start service:
sudo systemctl enable mqttSwitch.service \
sudo systemctl start mqttSwitch.service

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
