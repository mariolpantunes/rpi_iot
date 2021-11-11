#!/usr/bin/env python3
# coding: utf-8

__author__ = 'Mário Antunes'
__version__ = '0.1'
__email__ = 'mariolpantunes@gmail.com'
__status__ = 'Development'


import time
import signal
import logging
import argparse

import board
import adafruit_dht

import paho.mqtt.client as mqtt


# Configure the logging output
logging.basicConfig(level=logging.DEBUG, format='%(message)s')
logger = logging.getLogger(__name__)


# Global variable to control the flow
done = False


def signal_handler(sig, frame):
    logger.warning('You pressed Ctrl+C!')
    global done
    done = True


def main(args):
    # Graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initial the dht device, with data pin connected to:
    dhtDevice = adafruit_dht.DHT11(board.D4)

    # Create a MQTT client
    client = mqtt.Client()
    client.connect(args.u)

    while not done:
        try:
            # Print the values to the serial port
            temperature = dhtDevice.temperature
            humidity = dhtDevice.humidity
            logger.info(f'Temperature {temperature:.1f} C Humidity {humidity}%')
            client.publish('temperature', payload=temperature, qos=0, retain=False)
            client.publish('humidity', payload=humidity, qos=0, retain=False)
        except RuntimeError as error:
            # Errors happen fairly often, DHT's are hard to read, just keep going
            logger.warning(error.args[0])
            time.sleep(2.0)
            continue
        except Exception as error:
            dhtDevice.exit()
            raise error

        time.sleep(2.0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DHT11 app')
    parser.add_argument('-u', type=str, help='MQTT URL', default='localhost')
    args = parser.parse_args()
    
    main(args)
