import mqttConnect
import subprocess

def on_action():
    """
    When the request is ON, turn on the display
    """
    cmd = "sudo vcgencmd display_power 1"
    return(subprocess.call(cmd, shell=True))

def off_action():
    """
    When the request is OFF, turn off the display
    """
    cmd = "sudo vcgencmd display_power 0"
    return(subprocess.call(cmd, shell=True))

if __name__ == "__main__":
    # Set Topic to use
    userData = {"myTopic" : "mirror"}
    userData["onAction"] = on_action
    userData["offAction"] = off_action
    mqttConnect.main(userData)