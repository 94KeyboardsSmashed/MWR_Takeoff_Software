#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Python Data Collection Module

"""
Created on Tue May 9 12:13:27 2017

@author: Hyun-seok

IMPORTANT: REQUIRES ROOT ACCESS TO RUN.

Reads and interprets data from an ADXL 345 triaxial accelerometer and uses
a Adafruit 24 pixel neopixel ring to determine payload status.

Examples:
Run with the following lines on the command prompt:
    $ sudo python gnd.py

Run with this command to write to a .txt file:
    $ sudo nice -20 python gnd.py > logGND.txt

Wiring Details:

    Connect neopixel to ground, 5v, and physical pin 12 (gpio pin 18) (0)
    Connect neopixel to ground, 5v, and physical pin 33 (gpio pin 13) (1)

    GPIO 1 setup: ADXL - Pi (0x53)

    GND, SDO - GND
    VCC, CS - 3V3
    SDA - SDA (GPIO 2)
    SCL - SCL (GPIO 3)

    GPIO 2 setup: ADXL - Pi (0x1D)

    GND - GND
    VCC, CS, SDO - 3V3
    SDA - SDA
    SCL - SCL
"""

import sys
import collections
import time
from os import path
import raspi_accel_lib
import settings as st
import RPi.GPIO as GPIO
import datetime

if __name__ == '__main__':
    try:
        # init global variables
        CIRCULAR_BUFF = collections.deque(maxlen=st.MAXLEN)
        AVG_BUFF = collections.deque(maxlen=st.ACCEL_RESPONSE)
        RESTING = 0

        # Define accelerometers (named after rivers)
        YANGTZE = raspi_accel_lib.ADXL345(st.CAL_X, st.CAL_Y, st.CAL_Z, 0x53)

        # Startup Accelerometer
        YANGTZE.accel_startup(st.GFORCE)

        # Initalize Buzzer:
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(st.CHANNEL, GPIO.OUT)

        # Initalize .txt file by writing headers
        print ('# {}'.format(datetime.datetime.now().strftime("%a, %d %B %Y %I:%M:%S")))
        print('#Time,X,Y,Z')
        print('#{}'.format(YANGTZE.string_output(st.GFORCE)))
        sys.stdout.flush()

        # Store up data in circular buffer on launch pad and
        # flush when launched.
        start = time.time()
        counter = 1
        state = False

        while True:
            if time.time() - start > 0.1:
                start = time.time()
                counter = counter - 0.1
            
            if counter <= 0 and state == False:
                counter = 0.1
                state = True
            
            if counter <=0 and state == True:
                counter = 1
                state = False

            GPIO.output(st.CHANNEL, state)

            CIRCULAR_BUFF.append(YANGTZE.string_output(st.GFORCE))
            # If this accelerometer or other accelerometers in network detect launch. Very rudimentary at the moment.
            if YANGTZE.accel_magnitude(True) > st.TAKEOFF_THRESHOLD or path.getsize('logvdd.txt') > 1000:
                BUFFER_DATA = list(CIRCULAR_BUFF)
                print('\n'.join(BUFFER_DATA))
                sys.stdout.flush()
                break

        # Record Data until vehicle is deemed to be "landed"
        while True:
            print(YANGTZE.string_output(st.GFORCE))
            sys.stdout.flush()

            if YANGTZE.accel_magnitude(True) < st.LANDING_THRESHOLD:
                RESTING += 1
            elif st.LANDING_SENSE < 0:
                RESTING = 0
            else:
                RESTING -= st.LANDING_SENSE

            if RESTING <= 0:
                RESTING = 0

            if RESTING >= st.RESTING_THRESHOLD:
                print("#Landed")
                print("\x04")
                sys.stdout.flush()
                break
                            
            if path.getsize('loggnd.txt') > st.MEM_MAX:
                print('# Memory Stop')
                print("\x04")
                sys.stdout.flush()
                break

        sys.exit(0)
    except Exception as error:
        print ("#{}".format(error))
        sys.stdout.flush()
        sys.exit(2)
