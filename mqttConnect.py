import paho.mqtt.client as mqtt
import pwdCrypt.crypt as crypt
import json
import time

# Get the actual status and publish state_topic
def check_state(client, userdata):
  client.publish("{}{}".format(userdata["topic"]["~"], userdata["topic"]["stat_t"][1:]), payload = userdata["getStatus"](), qos=0, retain=True) 
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
    client.subscribe("{}{}".format(userdata["topic"]["~"], userdata["topic"]["cmd_t"][1:]))

    # Publish config message
    discoverable_topic = "{}/{}/{}/config".format(userdata["disc_topic"], userdata["type"], userdata["topic"]["~"])
    configPayload = json.dumps(userdata["topic"])
    client.publish(discoverable_topic, payload = configPayload, qos = 0, retain = True)
    # Publish availability topic
    client.publish("{}{}".format(userdata["topic"]["~"], userdata["topic"]["avty_t"][1:]), payload = "online", qos = 0, retain = True)
    #client.publish(userdata["myTopic"] + "/state_topic", payload = userdata["getStatus"](), qos=0, retain=True)
    # Update actual status
    check_state(client, userdata)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Trigger only on myTopic/request
    if (msg.topic+" "+str(msg.payload.decode()) == "{}{} ON".format(userdata["topic"]["~"], userdata["topic"]["cmd_t"][1:])):
        # Request ON action
        client.publish("{}{}".format(userdata["topic"]["~"], userdata["topic"]["stat_t"][1:]), payload = userdata["onAction"](), qos=0, retain=True)
    elif (msg.topic+" "+str(msg.payload.decode()) == "{}{} OFF".format(userdata["topic"]["~"], userdata["topic"]["cmd_t"][1:])):
        # Request OFF action
        client.publish("{}{}".format(userdata["topic"]["~"], userdata["topic"]["stat_t"][1:]), payload = userdata["offAction"](), qos=0, retain=True)

def main(userData):
    # Create instance with parameter
    client = mqtt.Client(userdata = userData)
    # Set LWT message: availability offline
    client.will_set("{}{}".format(userData["topic"]["~"], userData["topic"]["avty_t"][1:]), payload = "offline", qos = 0, retain = True)
    # Set callbacks
    client.on_connect = on_connect
    client.on_message = on_message
    
    client.username_pw_set(username = userData["user"], password = userData["password"])
    # Connect
    client.connect(userData["hostname"], userData["port"], 60)

    # Start loops
    client.loop_start()
    try:
      while True:
        check_state(client, userData)
        time.sleep(60)
    except KeyboardInterrupt:
      print('KeyboardInterrupt')

    client.loop_stop()
