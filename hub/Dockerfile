# Dockerfile that creates the image in docker desktop along with the required applications and copies the python code into it

# Use an existing base image to run the python environment

FROM python:3.11.1

# Add's a label to the container to easily identify the container later on

LABEL description="G2 DOCKER HUB"

# Copies the python code created into the docker container

COPY motionDevice_Copy.py ./

# Install the required python libraries for the code to run

RUN pip install paho-mqtt cryptography

# Set the command to run when the container is created and started

CMD ["python", "./motionDevice_Copy.py"]
