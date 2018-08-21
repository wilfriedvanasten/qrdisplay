#!/usr/bin/env python

import time
import sys
import getpass
import os.path as path
import RPi.GPIO as GPIO
from xdg.BaseDirectory import (save_config_path)
import configparser
import wifi


def wait_for_button_press(t=1000):
    c = GPIO.wait_for_edge(5, GPIO.FALLING, timeout=t)
    return c

def main():
    if len(sys.argv) > 2:
        print("Usage: qrdisplay [-d]")
        sys.exit(1)
    run_as_daemon = False
    if len(sys.argv) == 2:
        if sys.argv[1] == '-d':
            runAsDaemon = True
        else:
            print("Usage: qrdisplay [-d]")
            sys.exit(1)
    config = configparser.ConfigParser()

    config_path = save_config_path("qrdisplay")
    config_filename = path.join(config_path, "config")

    if not path.isfile(config_filename):
        if run_as_daemon:
            print("No config file exists yet. First run the program in the front so one can be created or create a config file at {}", config_file)
            sys.exit(1)
        else:
            print("Creating the config file")
            ssid = raw_input("SSID: ")
            key = getpass.getpass("Key: ")
            moonlight_host = raw_input("Moonlight Host: ")
            moonlight_arguments = raw_input("Moonlight Stream Arguments: ")
            config['WIFI'] = {
                    'ssid': ssid,
                    'key': key
                }
            config['Moonlight'] = {
                    'host': moonlight_host,
                    'arguments': moonlight_arguments
                }
            with open(config_filename, 'w') as config_file:
                config.write(config_file)
            sys.exit(0)
    else:
        config.read(config_filename)
        ssid = config['WIFI']['ssid']
        key = config['WIFI']['key']
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        wifi.display_qr_code(ssid, key)
        GPIO.add_event_detect(5, GPIO.FALLING, callback=wifi.create_event_callback(ssid, key))
        while True:
           try:
               time.sleep(30)
           except KeyboardInterrupt:
               GPIO.cleanup()
               raise
        

if __name__ == '__main__':
    main()
