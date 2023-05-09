
	2. HYPOTHESIS INVESTIGATION

2.1	Description

The team’s hypothesis question focused on achieving the basic cybersecurity requirement of authentication and authorisation within a microservice. can authentication and authorisation be handled within the code or should it be carried out and achieved as a different microservice on a separate container? (de Almeida, M.G. and Canedo, E.D., 2022.) discussed heavily that microservice should focus on dividing the application into small services, each running separately and connected through an (API) application programming interface gateway only when required. our hypothesis attempted to confirm if the authentication and authorisation processes can be added into the code without impacting the efficiency of the code. as MQTT connects the publisher and subscribers via a trusted broker in practice. which is often the case since IoT device owners often also are provided control over the broker and still require to validate the ownership via a username and password in order to login to the platform or pbe rovided with different commands. the hypothesis question attempts to find a direct answer to service discovery limitations as microservice architecture make service discovery hard especially when inter-service communication is required (Yarygina, T. and Bagge, A.H., 2018).

2.2	The Model

The current model proposed attempt to simplify the microservices function and code management, by integrating the authentication and authorisation function within the MQTT application running within docker as a container. This would remove the requirement of having a complex infrastructure such as integrating the docker simulation code with a (RADIUS) remote authentication dial in server or an Accesses control list. This model is meant to overcome the complexity of adding different containers as computing resources tend to be  limited and due to several hardware constraints the team wanted to simplify the approach and utilise of containers with a secure code depyloment and simplified access through the use of a basic username and password that is secure, functional and practical. 

2.3  Experiments and Analysis
Manually testing the application 
we attempted to login to the application without going into the signup process and it failed which is the desired result. this proved that the code was an efficient approach to achieve the result of authentication and authorisation processes. (Al-Naji, F.H. and Zagrouba, R., 2020) focused on the importance of authentication and authorisation within IoT devices as a continuous process. 

###Note: all figures are placed in the word document, if required the word document should be accessed to display the figures.###
 
Figure 2.1: Example of running the docker container with the MQTT code
 
Figure 2.2: Attempting to bypass the built-in authentication, which resulted in failure 

 
Figure 2.3: successfully loggin into the MQTT code after signing up to the application 
 
Figure 2.4: The code successfully running and simulating the motion sensor IoT


2.4 Python Script Testing with pylint
Pylint is an analysis tool that searches for errors, bugs, and other issues within Python code (Dasgupta & Hooshangi, 2017). To ensure our team’s Python code was secure, Pylint was used to test the code and improve each script. The initial code tests started with a score of 2.24 and was improved to reach the maximum score of 9.6
 
Figure 2.5: Pylint score for motion sensor and light clients before improvements.
 
Figure 2.6: Pylint score for motion sensor and light clients after improvements.
The pylint score increased from 6.00 to 9.60. The variable “rc” was left as it was as this is commonly used in other scripts. 

 
Figure 2.7: Light client simulator pylint score before improvements.
 
Figure 2.8: Light client simulator pylint after improvements.
 
Figure 2.9: Hub simulator pylint score before improvements.
 
Figure 2.10: Hub simulator pylint after before improvements.
These scores show a large improvement in each of the scripts, allowing for more efficient code using best practices. 
2.5 Docker Vulnerability test

The test can only be carried out after building the image, then go to the container tab and selecting view image, several vulnerabilities were identified by Docker as it built the images with the most stable release of the Debian OS.

 
Figure 2.11:  List of 243 identified vulnerabilities within the Docker Image 

 
Figure 2.12: The above image is for the Debian destroy utilised within docker

 
Figure 2.13: The above image is for vulnerabilities with python 3.11 and used libraries.

2.6 Bandit Testing 

Step 1: install bandit with the following command:
	Pip install bandit
Step 2: run the following command to test the python code 
	Bandit -r motionDevice_Copy.py

 
Figure 2.14: installing bandit

 
Figure 2.15: Running Bandit test on our python code

Final Bandit output:

Test results:
>> Issue: [B311:blacklist] Standard pseudo-random generators are not suitable for security/cryptographic purposes.
   Severity: Low   Confidence: High
   CWE: CWE-330 (https://cwe.mitre.org/data/definitions/330.html)
   Location: motionDevice_Copy.py:110:38


2.7	Conclusion
We have concluded that the hypothesis requires more time to test and confirm if authentication and authorization can be carried out within python efficiently without the assistance of additional microservices adding further complexity to the simulation. although the desired result was achieved, further evidence such as log’s and appropriate checks on the security of the authentication and authorisation, was not achieved as it broke the MQTT code and stopped the main objective was to simulate the IoT environment required for a smart home light system. 
Recommendations and improvements:
•	Physical network/VPN for ultimate security; to connect the IoT devices with a master control hub in a secure manner. 
•	(TLS) Transport layer security with certificate credentials from CA for all connections;
•	All inbound ports should be disabled at MQTT edge clients; and additionally restricted with a firewall access list implementation. 
•	Only two TCP/IP ports (8883 and 443) should be open at the MQTT server;
•	Use MQTT client username/password at MQTT servers; and ensure audit trails are stored separately for forensic use if required. 
•	ACLs should be used to limit MQTT client access to the topic levels they can either publish or subscribe to.
•	Enable the use of biometric authentication prior to access of the MQTT platform / Smarthome system to ease the login process of the user. 




3.	HOW TO / CODE INSTRUCTIONS/SOURCE CODE
Requirements and setup/ running the application guideline
Install docker desktop on windows available from: https://www.docker.com/products/docker-desktop/
Install python for windows, available from: https://www.python.org/downloads/  current version in use is 3.11
Steps to run the microservices applications:
1.	Navigate to the folder SSA_DockerProject with CMD
a.	One terminal window should be dedicated to running the Hub Docker file
b.	One terminal window should be dedicated to running the Light Docker file
2.	Within the first command line window run the command to build the docker image 
1.	docker build -t g2-mqtt-hub .      # command is used to build the image
2.	docker run -i -t g2-mqtt-hub       # command is used to run the container

When deleting the images on docker first start with deleting the container, then delete the image when it's no longer required in that order. 

download paho.mqtt by running 
    pip install paho-mqtt

to run a pyscript use cmd terminal and run the name of the script eg. lightControl.py
then run the python file

#MQTT Subscriber

import paho.mqtt.client as mqtt
import sys

def onMessage(client, userdata, msg):
    print( msg.payload.decode())

client =mqtt.Client()
client.on_message = onMessage

if client.connect("localhost", 1883, 60) != 0:
    print("Could not connect to MQTT Broker!")
    sys.exit(-1)

client.subscribe("lightstate")

try:
    print("Press CTRL+C to exit....")
    client.loop_forever()
except:
    print("Disconnecting from broker")

client.disconnect()

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

# If motion was detected, it also publishes a message to turn on the light by publishing an "on" message to the "light_control" topic.
# The loop then waits for 5 seconds before repeating.

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

# Start the MQTT loop indefinitely to listen and handle messages
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


4.0 REFERENCES

de Almeida, M.G. and Canedo, E.D., 2022. Authentication and authorization in microservices architecture: A systematic literature review. Applied Sciences, 12(6), p.3023.

Yarygina, T. and Bagge, A.H., 2018, March. Overcoming security challenges in microservice architectures. In 2018 IEEE Symposium on Service-Oriented System Engineering (SOSE) (pp. 11-20). IEEE.

Al-Naji, F.H. and Zagrouba, R., 2020. A survey on continuous authentication methods in Internet of Things environment. Computer Communications, 163, pp.109-133.


5.0	CODE REFERENCES
Anon, 2021. Developing inside a Docker Container in Visual Studio Code. [Online] Available at: https://francescopochetti.com/developing-inside-a-docker-container-in-visual-studio-code/ [Accessed 8 February 2023].
Bender, M., et al, 2021,. ‘Open-source mqtt evaluation.’, 18th Annual Consumer Communications & Networking Conference, pp. 1-4. IEEE.
Cope, S., N.D.. How to Use The Paho MQTT Python Client for Beginners. [Online] Available at: http://www.steves-internet-guide.com/into-mqtt-python-client/ [Accessed 11 February 2023].
 How to hash, salt and verify passwords in NodeJs, python Golan and Java. (supertokens team, 2022) available at: https://supertokens.com/blog/password-hashing-salting [Accessed on 27 February, 2023]
Joy, A., N.D.. A Deep Dive Into Fernet Module in Python. [Online] Available at: https://pythonistaplanet.com/fernet/ [Accessed 20 February 2023].
PyPi, N.D.. paho-mqtt 1.6.1. [Online] Available at: https://pypi.org/project/paho-mqtt/#:~:text=This%20code%20provides%20a%20client,.9%2B%20or%203.6%2B. [Accessed 26 February 2023].
Python (2023). ‘sys – System-specific parameters and functions’, Python. [Online]  Available at: https://docs.python.org/3/library/sys.html [Accessed: 28/02/2023]
Python login and signup, Available at: https://github.com/br34th3r/PythonLoginAndRegister [Accessed on 26 February 2023]
Python program to check the validity of a password (2023), available at: https://www.geeksforgeeks.org/python-program-check-validity-password/ [Accessed on 26 Febraury 2023]
TutorialsTeacher (2023). ‘Python – Random Module’, TutorialsTeacher. [Online] Available at: https://www.tutorialsteacher.com/python/random-module#:~:text=The%20random%20module%20is%20a,%2C%20shuffle%20elements%20randomly%2C%20etc. [Accessed: 28/02/2023]
