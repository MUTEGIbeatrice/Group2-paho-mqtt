# This Python script uses the MQTT (Message Queuing Telemetry Transport) protocol to communicate between a motion sensor device and a light control system. 
# The script consists of two parts: one for the motion sensor device (motionDevice.py) and one for the light control system (lightControl.py).

# This is the first part of the script (motionDevice.py), which runs on the motion sensor device.



#Import of the libraries
import paho.mqtt.client as mqtt #for MQTT protocol
import time #to simulate IoT delays
import random #to create random id
import json #to convert the python dictionary into a JSON string that can be written into a file

# Set up the device's ID and type
device_id = "Device_001"
device_type = "motion_sensor"

# Define the on_connect and on_publish functions for the MQTT client
def on_connect(client, userdata, flags, rc): #rc (return code) is used for checking that the connection was established.
    print("Connected to broker with result code "+str(rc))

def on_publish(client, userdata, mid): #mid value is an integer that corresponds to the published message number as assigned by the client.
    print("Message published with mid "+str(mid))

# Create MQTT client instance
client = mqtt.Client()

#Assign the on_connect and on_publish functions to it
client.on_connect = on_connect
client.on_publish = on_publish

# Connect to the MQTT broker
client.connect("mqtt.eclipseprojects.io") # a public test MQTT broker address/service "https://mqtt.eclipseprojects.io/ "

# Loop indefinitely
while True:
    # Simulate motion detection by randomly selecting True or False
    motion_detected = random.choice([True, False])
    
    # Create a dictionary containing the device's ID, type, and whether motion was detected
    data = {
        "device_id": device_id,
        "device_type": device_type,
        "motion_detected": motion_detected
    }
    
    # Convert the dictionary to a JSON string and publish it to the "motion_sensor" topic
    payload = json.dumps(data)
    print("Publishing: " + payload)
    client.publish("motion_sensor", payload)
    
    # If motion was detected, also publish a message to turn on the light
    if motion_detected:
        print("Motion detected! Lights on")
        client.publish("light_control", "on")
    else:
        print("No motion detected.")
    
    # Wait for 5 seconds before repeating the loop
    time.sleep(5)




#CODE SUMMARY:

# It starts by importing the required libraries then it defines the MQTT broker parameters/connection and sets up the device's ID and type. 
# It also defines the on_connect and on_publish functions for the MQTT client, which are called when the client connects to the broker and publishes a message, respectively. 
# The script creates an MQTT client instance, assigns the on_connect and on_publish functions to it, and connects to the MQTT broker. 
# The script then enters an infinite loop where it simulates motion detection by randomly selecting True or False, 
# creates a dictionary containing the device's ID, type, and whether motion was detected, 
# converts the dictionary to a JSON string, and publishes it to the "motion_sensor" topic. 

# If motion was detected, it also publishes a message to turn on the light by publishing a "on" message to the "light_control" topic.
# The loop then waits for 5 seconds before repeating.