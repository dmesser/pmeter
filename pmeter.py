from pms7003 import Pms7003Sensor, PmsSensorException
from influxdb import InfluxDBClient
import time
import os
import sys
import socket


def createInfluxPoint(data):
    if type(data) is dict:

        return {
            "measurement": "particulate-matter",
            "tags": {
                "hostname": socket.gethostname()
            },
            "fields": data
        }
        
    else:
        raise TypeError("Expected dictionary but got %s" % type(data))


def writeParticleData(data):
    if type(data) is dict:

        point = createInfluxPoint(data)

        client = InfluxDBClient(host=influxHost, port=influxPort, username=influxUser,
                                password=influxPassword, database=influxDB, ssl=True, verify_ssl=True)

        client.write_points([point])

        client.close()

    else:
        raise TypeError("Expected dictionary but got %s" % type(data))


if __name__ == '__main__':

    influxHost = os.getenv("INFLUXDB_HOST")
    influxPort = os.getenv("INFLUXDB_PORT")
    influxDB = os.getenv("INFLUXDB_DB")
    influxUser = os.getenv("INFLUXDB_USER")
    influxPassword = os.getenv("INFLUXDB_PASSWORD")

    if None in (influxHost, influxPort, influxDB, influxUser, influxPassword):
        print("Incomplete database credentials", file=sys.stderr)
        exit(1)
    else:
        print("Sending telemetry to InfluxDB %s on port %s using TLS as user %s" % (influxHost, influxPort, influxUser))

    sensorDevice = os.getenv("DEVICE", default="/dev/ttyUSB0")
    print("Using device %s" % sensorDevice)

    print("Reporting as %s" % socket.gethostname())

    sensor = Pms7003Sensor(sensorDevice)

    while True:
        try:
            data = sensor.read()
            writeParticleData(data)
            time.sleep(2)
        except PmsSensorException:
            print('Sensor exception')
        except ConnectionError:
            print('Database exception')

    sensor.close()
