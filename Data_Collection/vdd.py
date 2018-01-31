#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Python Data Collection Module

"""
Created on Tue May  9 12:13:27 2017

@author: Hyun-seok

Please use indents as they are incompatible with spaces
and spaces are a pain in the arse to do 5 times for every indent.

IMPORTANT: REQUIRES ROOT ACCESS TO RUN.

Connect neopixel to ground, 5v, and physical pin 12 (gpio pin 18) (0)
Connect neopixel to ground, 5v, and physical pin 33 (gpio pin 13) (1)

GPIO 1 setup: ADXL - Pi (0x53)

GND - GND
3V - 3V3
SDA - SDA (GPIO 2)
SCL - SCL (GPIO 3)

GPIO 2 setup: ADXL - Pi (0x1D)

GND - GND
3V - 3V3
SDA - SDA
SCL - SCL
SDO - GND
"""

import sys
import time
import collections
import raspi_accel_lib
import neopixel_lib as neopxl

##Accelerometer Settings:
#Max Capacity for circular buffer memory
MAXLEN = 2700

#Output readings in Gs, set to false if measurments in m/s**2 is desired
GFORCE = False

#Amount of acceleration smoothing needed
ACCEL_RESPONSE = 10

#Amount of Gs needed to register vehicle liftoff
TAKEOFF_THRESHOLD = 3

#Amount of G deviation from zero that counts the vehicle as 'landed'
LANDING_THRESHOLD = 0.5

#Amount subtracted from landing count when bumped. Set negative number to reset from 0
LANDING_SENSE = -1

#Number of consecutive lines needed
#below the Landing Threshold for the accelerometer to stop recording
RESTING_THRESHOLD = 2500

##Neopixel Settings
#Amount of time needed in testing stage (seconds)
TEST_LENGTH = 10

#Neopixel Ring Hardware Constants
LED_COUNT_1 = 24
LED_PIN_1 = 13
LED_FREQ_HZ_1 = 800000
LED_DMA_1 = 5
LED_BRIGHTNESS_1 = 255
LED_INVERT_1 = False

#Color Values
RED = neopxl.color_value(255, 0, 0)
GREEN = neopxl.color_value(0, 255, 0)
BLUE = neopxl.color_value(0, 0, 255)
MAGENTA = neopxl.color_value(255, 0, 255)

if __name__ == '__main__':
    # init global variables
    CIRCULAR_BUFF = collections.deque(maxlen=MAXLEN)
    AVG_BUFF = collections.deque(maxlen=ACCEL_RESPONSE)
    RESTING = 0

    # Define accelerometers (named after rivers)
    INDUS = raspi_accel_lib.ADXL345(0x1D)

    # Define Neopixels (named after swords)
    KATANA = neopxl.Adafruit_NeoPixel(LED_COUNT_1, LED_PIN_1, LED_FREQ_HZ_1,
                                      LED_DMA_1, LED_INVERT_1, LED_BRIGHTNESS_1, 1)

    # Startup Neopixel
    KATANA.neopixel_startup(BLUE, GREEN)

    # Startup Accelerometer
    print(INDUS.accel_startup(GFORCE))
    sys.stdout.flush()

    # Make testable at start
    TEST_TIMER = time.time() + TEST_LENGTH

    while time.time() < TEST_TIMER:
        #Process light color by finding averages
        PER = INDUS.accel_magnitude()*10
        if PER > 100:
            PER = 100
        AVG_BUFF.append(PER)
        MAG_AVG = sum(list(AVG_BUFF))/len(list(AVG_BUFF))

        #Show averages on color gradient
        KATANA.color_gradient_rg(MAG_AVG)
    # Shutdown neopixel rings
    KATANA.neopixel_shutdown(MAGENTA)

    # Store up data in circular buffer on launch pad and
    # flush when launched.
    while True:
        CIRCULAR_BUFF.append(INDUS.string_output())
        if INDUS.accel_magnitude(True) > TAKEOFF_THRESHOLD:
            BUFFER_DATA = list(CIRCULAR_BUFF)
            print('\n'.join(BUFFER_DATA))
            sys.stdout.flush()
            break

    # Record Data until vehicle is deemed to be "landed"
    while True:
        print(INDUS.string_output(GFORCE))
        sys.stdout.flush()

        if INDUS.accel_magnitude(True) < LANDING_THRESHOLD:
            RESTING += 1
        elif LANDING_SENSE < 0:
            RESTING = 0
        else:
            RESTING -= LANDING_SENSE

        if RESTING <= 0:
            RESTING = 0

        if RESTING >= RESTING_THRESHOLD:
            print("#Landed")
            sys.stdout.flush()
            break
