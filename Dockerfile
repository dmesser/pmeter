FROM python:3.7.9-buster

ENV INFLUXDB_HOST="" \
    INFLUXDB_PORT="" \
    INFLUXDB_DB="" \
    INFLUXDB_USER="" \
    INFLUXDB_PASSWORD="" \
    DEVICE="/dev/ttyUSB0"

COPY pmeter.py requirements.txt /app/
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "pmeter.py"] 