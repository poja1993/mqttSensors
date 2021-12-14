import paho.mqtt.client as mqtt
import pwdCrypt.crypt as crypt
import json
import time
from threading import Timer

def create_config_payload(userdata):
    device = {}
    device["identifiers"] = ["magic_mirror"]
    device["name"] = userdata["name"]
    device["model"] = "-"
    device["manufacturer"] = "Gabi"

    config = {}
    config["~"] = userdata["myTopic"]
    config["uniq_id"] = userdata["myTopic"]
    config["name"] = userdata["name"]
    config["cmd_t"] = "~/request"
    config["stat_t"] = "~/state_topic"
    config["avty_t"] = "~/availability"
    config["device"] = device
    return json.dumps(config)

# Get the actual status and publish state_topic
def check_state(client, userdata):
  client.publish(userdata["myTopic"] + "/state_topic", payload = userdata["getStatus"](), qos=0, retain=True) 
  print("State checked")

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    connect_dict = {
    0: "Connection successful",
    1: "Connection refused - incorrect protocol version",
    2: "Connection refused - invalid client identifier",
    3: "Connection refused - server unavailable",
    4: "Connection refused - bad username or password",
    5: "Connection refused - not authorised"
    }
    print(connect_dict[rc])

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(userdata["myTopic"] + "/request")

    discoverable_topic = "homeassistant/" + userdata["type"] + "/" + userdata["myTopic"]
    # Publish config {"device_class":"temperature","name":"raspi3 Temperature","state_topic":"system-sensors/sensor/raspi3/state","unit_of_measurement":"°C","value_template":"{{value_json.temperature}}","unique_id":"raspi3_sensor_temperature","availability_topic":"system-sensors/sensor/raspi3/availability","device":{"identifiers":["raspi3_sensor"],"name":"raspi3 Sensors","model":"RPI raspi3", "manufacturer":"RPI"},"icon":"mdi:thermometer"}
    configPayload = create_config_payload(userdata)
    client.publish(discoverable_topic + "/config", payload = configPayload, qos = 0, retain = True)
    # Publish availability topic
    client.publish(userdata["myTopic"] + "/availability", payload = "online", qos = 0, retain = True)
    #client.publish(userdata["myTopic"] + "/state_topic", payload = userdata["getStatus"](), qos=0, retain=True)
    check_state(client, userdata)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Trigger only on myTopic/request
    if (msg.topic+" "+str(msg.payload.decode()) == userdata["myTopic"] + "/request ON"):
        # Request ON action
        client.publish(userdata["myTopic"] + "/state_topic", payload = userdata["onAction"](), qos=0, retain=True)
    elif (msg.topic+" "+str(msg.payload.decode()) == userdata["myTopic"] + "/request OFF"):
        # Request OFF action
        client.publish(userdata["myTopic"] + "/state_topic", payload = userdata["offAction"](), qos=0, retain=True)

def main(userData):
    # Create instance with parameter
    client = mqtt.Client(userdata = userData)
    # Set LWT message: availability offline
    client.will_set(userData["myTopic"] + "/availability", payload = "offline", qos = 0, retain = True)
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    # Get user info from Json
    cryp = crypt.pwdCrypt()
    data = cryp.get_user_info()
    client.username_pw_set(username = data["user"], password = data["password"])
    # Connect
    client.connect(data["hostname"], data["port"], 60)

    # Start loops
    client.loop_start()
    try:
      while True:
        check_state(client, userData)
        time.sleep(60)
    except KeyboardInterrupt:
      print('KeyboardInterrupt')

    client.loop_stop()
