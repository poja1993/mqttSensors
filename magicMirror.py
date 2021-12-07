import mqttConnect

def on_action():
    print("On Action")

def off_action():
    print("Off Action")

if __name__ == "__main__":
    # Set Topic to use
    userData = {"myTopic" : "mirror"}
    userData["onAction"] = on_action
    userData["offAction"] = off_action
    mqttConnect.main(userData)