#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import time
import enum
import signal
import logging
import argparse

import board
import adafruit_dht
import adafruit_bmp280

import paho.mqtt.client as mqtt


# Configure the logging output
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)


# Global variable to control the flow
done = False
refresh = 2


# Enum for the sensor type
class Sensor(enum.Enum):
    dht11='dht11'
    bmp280='bmp280'

    def __str__(self):
        return self.value


def signal_handler(sig, frame):
    logger.warning('You pressed Ctrl+C!')
    global done
    done = True


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info('Connected to MQTT Broker!')
        # Subscribe the command topic
        client.subscribe('dht11/cmd')
    else:
        logger.warning(f'Failed to connect, return code {rc}')


def on_message(client, userdata, msg):
    global refresh
    payload = msg.payload.decode()
    topic = msg.topic
    logger.info(f'Received {payload} from {topic} topic')
    refresh = float(payload)


def main(args):
    global refresh
    
    # Graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)

    if args.s is Sensor.dht11:
        # Initial the dht device, with data pin connected to:
        sensor = adafruit_dht.DHT11(board.D4)
    elif args.s is Sensor.bmp280:
        i2c = board.I2C()  # uses board.SCL and board.SDA
        sensor = adafruit_bmp280.Adafruit_BMP280_I2C(i2c)
        sensor.sea_level_pressure = 1013.25

    # Create a MQTT client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(args.u)
    client.loop_start()

    while not done:
        try:
            # Print the values to the serial port
            temperature = sensor.temperature
            
            client.publish(f'{args.s}/temperature', payload=temperature, qos=0, retain=False)
            if args.s is Sensor.dht11:
                humidity = sensor.humidity
                client.publish(f'{args.s}/humidity', payload=humidity, qos=0, retain=False)
                logger.info(f'Temperature {temperature:.1f} C Humidity {humidity}%')
            elif args.s is Sensor.bmp280:
                pressure = sensor.pressure
                client.publish(f'{args.s}/pressure', payload=pressure, qos=0, retain=False)
                altitude = sensor.altitude
                client.publish(f'{args.s}/altitude', payload=altitude, qos=0, retain=False)
                logger.info(f'Temperature {temperature:.1f} C Pressure {pressure:.1f} hPa Altitude {altitude:.2f} meters')

        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            logger.warning(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            if args.s is Sensor.dht11:
                sensor.exit()
            raise error

        time.sleep(refresh)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DHT11 app')
    parser.add_argument('-u', type=str, help='MQTT URL', default='localhost')
    parser.add_argument('-s', help='Sensor type', type=Sensor, choices=list(Sensor), default='dht11')
    args = parser.parse_args()
    
    main(args)
