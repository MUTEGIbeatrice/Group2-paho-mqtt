# Dockerfile, Image, Container

FROM python:3.11.1

LABEL description="G2 DOCKER LIGHT"

COPY lightControl_copy.py ./

RUN pip install paho-mqtt cryptography

CMD ["python", "./lightControl_copy.py"]
