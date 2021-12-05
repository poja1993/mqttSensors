import paho.mqtt.client as mqtt
import crypt

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
    client.publish(userdata["myTopic"] + "/availability", payload = "online", qos = 0, retain = True)
    client.subscribe(userdata["myTopic"] + "/request")
    

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload.decode()))
    if (msg.topic+" "+str(msg.payload.decode()) == userdata["myTopic"] + "/request ON"):
        print("state_topic on")
        client.publish(userdata["myTopic"] + "/state_topic", payload="ON", qos=0, retain=False)
    elif (msg.topic+" "+str(msg.payload.decode()) == userdata["myTopic"] + "/request OFF"):
        print("state_topic off")
        client.publish(userdata["myTopic"] + "/state_topic", payload="OFF", qos=0, retain=False)

def main():
    userData = {"myTopic" : "mirror"}
    client = mqtt.Client(userdata = userData)
    client.will_set(userData["myTopic"] + "/availability", payload = "offline", qos = 0, retain = True)
    client.on_connect = on_connect
    client.on_message = on_message
    data = crypt.get_user_info()
    client.username_pw_set(username = data["user"], password = data["password"])

    client.connect(data["hostname"], data["port"], 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

if __name__ == "__main__":
    main()