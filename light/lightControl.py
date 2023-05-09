# This Python script uses the MQTT (Message Queuing Telemetry Transport) protocol to communicate between a motion sensor device and a light control system.
# The script consists of two parts: one for the motion sensor device (motionDevice.py) and one for the light control system (lightControl.py).

#This is the second part of the script (lightControl.py), which runs on the light control system.



#Import libraries
import paho.mqtt.client as mqtt #for MQTT protocol
import json #to convert the python dictionary into a JSON string that can be written into a file

# Set up the initial state of the light
light_state = "off"

# Define the on_connect and on_message functions for the MQTT client
def on_connect(client, userdata, flags, rc):
    print("Connected to broker with result code "+str(rc))

    # Subscribe to the "motion_sensor" and "light_control" topics
    client.subscribe("motion_sensor")
    client.subscribe("light_control")

def on_message(client, userdata, message):
    # Extract the topic and payload from the received message
    global light_state
    topic = message.topic
    payload = message.payload.decode()
    print("Received message: "+payload+" on topic: "+topic)

    # If the message is from the motion sensor, check if motion was detected and turn on the light if it's currently off
    if topic == "motion_sensor":
        data = json.loads(payload)
        motion_detected = data["motion_detected"]
        if motion_detected:
            print("Motion detected!")
            if light_state == "off":
                client.publish("light_control", "on")
                print("Turning on the light.")
                light_state = "on"
        else:
            print("No motion detected.")

    # If the message is a light control message, update the state of the light accordingly
    elif topic == "light_control":
        if payload == "on":
            print("Light turned on.")
            light_state = "on"
        elif payload == "off":
            print("Light turned off.")
            light_state = "off"

# Create MQTT client instance
client = mqtt.Client()

# Assign the on_connect and on_message functions to MQTT client instance
client.on_connect = on_connect
client.on_message = on_message # Set up callback function for message received event

# Connect to the MQTT broker
client.connect("mqtt.eclipseprojects.io") # a public test MQTT broker address/service "https://mqtt.eclipseprojects.io/ "


# Subscribe to the motion detection topic and define callback
client.subscribe("home/light")


# Start the MQTT loop indefinately to listen and handle messages
client.loop_forever()




# CODE SUMMARY:

# It starts by importing the required libraries, including the Paho MQTT client library and JSON and defines the MQTT broker parameters,
# sets up the initial state of the light, and defines the on_connect and on_message functions for the MQTT client.
# The on_connect function is called when the client connects to the broker and subscribes to the "motion_sensor" and "light_control" topics.
# The on_message function is called when the client receives a message, extracts the topic and payload from the received message,
# and checks if the message is from the motion sensor or the light control system.
# If the message is from the motion sensor, it checks if motion was detected and turns on the light if it's currently off.
# If the message is a light control message, it updates the state of the light accordingly.
# The script creates an MQTT client instance, assigns the on_connect and on_message functions to it, and connects to the MQTT broker.
# The script then starts the MQTT loop indefinitely to listen and handle messages.