import mqttConnect

if __name__ == "__main__":
    # Set Topic to use
    userData = {"myTopic" : "mirror"}
    mqttConnect.main(userData)