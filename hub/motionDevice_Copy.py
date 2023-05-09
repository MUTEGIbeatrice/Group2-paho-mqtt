# This Python script uses the MQTT (Message Queuing Telemetry Transport) protocol to communicate between a motion sensor device and a light control system. 
# The script consists of two parts: one for the motion sensor device (motionDevice.py) and one for the light control system (lightControl.py).
# This is the first part of the script (motionDevice.py), which runs on the motion sensor device.

#Import of the libraries
import paho.mqtt.client as mqtt #for MQTT protocol
import time #to simulate IoT delays
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
            

#CODE SUMMARY:

# It starts by importing the required libraries then it defines the MQTT broker parameters/connection and sets up the device's ID and type. 
# It also defines the on_connect and on_publish functions for the MQTT client, which are called when the client connects to the broker and publishes a message, respectively. 
# The script creates an MQTT client instance, assigns the on_connect and on_publish functions to it, and connects to the MQTT broker. 
# The script then enters an infinite loop where it simulates motion detection by randomly selecting True or False, 
# creates a dictionary containing the device's ID, type, and whether motion was detected, 
# converts the dictionary to a JSON string, and publishes it to the "motion_sensor" topic. 

# If motion was detected, it also publishes a message to turn on the light by publishing a "on" message to the "light_control" topic.
# The loop then waits for 5 seconds before repeating.