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
    $ sudo python vdd.py

Run with this command to write to a .txt file:
    $ sudo nice -20 python vdd.py > logVDD.txt

Wiring Details:

    GPIO 1 setup: ADXL - Pi (0x53)

    GND - GND
    3V - 3V3
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
import datetime
from os import path
import raspi_accel_lib
import settings as st

if __name__ == '__main__':
    try:
        # init global variables
        CIRCULAR_BUFF = collections.deque(maxlen=st.MAXLEN)
        AVG_BUFF = collections.deque(maxlen=st.ACCEL_RESPONSE)
        RESTING = 0

        # Define accelerometers (named after rivers)
        INDUS = raspi_accel_lib.ADXL345(st.CAL_X, st.CAL_Y, st.CAL_Z, 0x1D)

        # Startup Accelerometer
        INDUS.accel_startup(st.GFORCE)
        sys.stdout.flush()

        #Initalize .txt file by writing headers
        print ('# {}'.format(datetime.datetime.now().strftime("%a, %d %B %Y %I:%M:%S")))

        print('#Time,X,Y,Z')
        print("#{}".format(INDUS.string_output(st.GFORCE)))
        sys.stdout.flush()

        # Store up data in circular buffer on launch pad and
        # flush when launched.
        while True:
            CIRCULAR_BUFF.append(INDUS.string_output(st.GFORCE))
            # If this accelerometer or other accelerometers in network detect launch. Very rudimentary at the moment.
            if INDUS.accel_magnitude(True) > st.TAKEOFF_THRESHOLD or path.getsize('loggnd.txt') > 1000:
                BUFFER_DATA = list(CIRCULAR_BUFF)
                print('\n'.join(BUFFER_DATA))
                sys.stdout.flush()
                break

        # Record Data until vehicle is deemed to be "landed"
        while True:
            print(INDUS.string_output(st.GFORCE))
            sys.stdout.flush()

            if INDUS.accel_magnitude(True) < st.LANDING_THRESHOLD:
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
		
            if path.getsize('logvdd.txt') > st.MEM_MAX:
                print('# Memory Stop')
                print("\x04")
                break
        sys.exit(0)
    except Exception as error:
        print("# {}".format(error))
        sys.exit(1)
