#!/usr/bin/env python

import time
import sys
import getpass
import os.path as path
import RPi.GPIO as GPIO
from gpiozero import Button
from xdg.BaseDirectory import (save_config_path)
import configparser
import wifi


def main():
    config = configparser.ConfigParser()

    config_path = save_config_path("qrdisplay")
    config_filename = path.join(config_path, "config")

    if not path.isfile(config_filename):
        print("Creating the config file")
        ssid = raw_input("SSID: ")
        key = getpass.getpass("Key: ")
        config['WIFI'] = {
            'ssid': ssid,
            'key': key
        }
        with open(config_filename, 'w') as config_file:
            config.write(config_file)
        sys.exit(0)
    else:
        config.read(config_filename)
        ssid = config['WIFI']['ssid']
        key = config['WIFI']['key']
        GPIO.setmode(GPIO.BCM)
        wifi.display_qr_code(ssid, key)
        wifi_button = Button(5)
        wifi_button.when_pressed = wifi.create_event_callback(ssid, key)
        while True:
            time.sleep(30)
        

if __name__ == '__main__':
    main()
