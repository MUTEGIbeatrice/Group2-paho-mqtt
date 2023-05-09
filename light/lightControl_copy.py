# This Python script uses the MQTT (Message Queuing Telemetry Transport) protocol to communicate between a motion sensor device and a light control system.
# The script consists of two parts: one for the motion sensor device (motionDevice.py) and one for the light control system (lightControl.py).

#This is the second part of the script (lightControl.py), which runs on the light control system.



#Import libraries
import paho.mqtt.client as mqtt #for MQTT protocol
import json #to convert the python dictionary into a JSON string that can be written into a file
import random #to create random id
import json #to convert the python dictionary into a JSON string that can be written into a file
import getpass #to get input from user without printing the username/pass on screen
import hashlib #hash password to storage
from cryptography.fernet import Fernet


# Generate a unique key that is used for for encryption and decryption of the data
key = Fernet.generate_key()

def get_password_hash(password):
    
    #Generates password that is hashed using a SHA-256 encryption

    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_password(password):
    
    #uses the encrypted version of the password that was entred using the Fernet key
    
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    """
    Returns the decrypted version of the password using the Fernet key
    """
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

def validate_password(password):
    
    #Password validation function that gives out true if it meets the requirments or false if it doesn't
    
    if len(password) < 8:
        return False
    elif not any(char.isdigit() for char in password):
        return False
    elif not any(char.isupper() for char in password):
        return False
    elif not any(char.islower() for char in password):
        return False
    else:
        return True

def signup():
    
    #Allows the user to create an account within the microservice with username and password that is saved in a txt file, 
    #the username will be showen but the password will be encrypted
    
    username = input("Please Enter a username: ")
    while True:
        password = getpass.getpass("Please Enter a password (must be at least 8 characters and contain at least one digit, one uppercase letter, and one lowercase letter): ")
        if validate_password(password):
            break
        else:
            print("Invalid password. Please try again.")
    password_hash = get_password_hash(password)
    encrypted_password = encrypt_password(password)
    with open("DB.txt", "a") as f:
        f.write(f"{username}:{password_hash}:{encrypted_password}\n")

def login():
    
    #used to login into the application with the previously created username and password selected
    
    attempts = 0
    while attempts < 3:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        password_hash = get_password_hash(password)
        with open("DB.txt", "r") as f:
            for line in f:
                stored_username, stored_password_hash, encrypted_password = line.strip().split(":")
                if stored_username == username and stored_password_hash == password_hash:
                    decrypted_password = decrypt_password(encrypted_password)
                    if decrypted_password == password:
                        print("Login successful!")

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

return

print("Invalid username or password. Please try again.")
    attempts += 1
    print("Maximum login attempts reached. Exiting program.")
    exit()

while True:
    choice = input("Enter '1' to sign up, '2' to log in, or 'q' to quit: ")
    if choice == "1":
        signup()
    elif choice == "2":
        login()
    elif choice == "q":
        break
    else:
        print("Invalid choice.")




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