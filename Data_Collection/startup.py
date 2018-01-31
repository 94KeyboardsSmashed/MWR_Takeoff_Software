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
#Output readings in Gs, set to false if measurments in m/s**2 is desired
GFORCE = False

#Amount of acceleration smoothing needed
ACCEL_RESPONSE = 10

##Neopixel Settings
#Amount of time needed in testing stage (seconds)
TEST_LENGTH = 10

#Neopixel Ring Hardware Constants
LED_COUNT_1 = 24
LED_PIN_1 = 18
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
    IAVG_BUFF = collections.deque(maxlen=ACCEL_RESPONSE)
    YAVG_BUFF = collections.deque(maxlen=ACCEL_RESPONSE)

    # Define accelerometers (named after rivers)
    INDUS = raspi_accel_lib.ADXL345(0x1D)
    YANGTZE = raspi_accel_lib.ADXL345(0x53)

    # Define Neopixels (named after swords)
    KATANA = neopxl.Adafruit_NeoPixel(LED_COUNT_1, LED_PIN_1, LED_FREQ_HZ_1,
                                      LED_DMA_1, LED_INVERT_1, LED_BRIGHTNESS_1, 0)

    # Startup Neopixel
    KATANA.neopixel_startup(BLUE, GREEN)

    # Startup Accelerometer
    print(INDUS.accel_startup(GFORCE))
    print(YANGTZE.accel_startup(GFORCE))

    # Make testable at start
    TEST_TIMER = time.time() + TEST_LENGTH

    while time.time() < TEST_TIMER:
        #Process light color by finding averages
        INDUS_PER = INDUS.accel_magnitude()*10
        if INDUS_PER > 100:
            INDUS_PER = 100
        IAVG_BUFF.append(INDUS_PER)
        IMAG_AVG = sum(list(IAVG_BUFF))/len(list(IAVG_BUFF))

        YANGTZE_PER = INDUS.accel_magnitude()*10
        if YANGTZE_PER > 100:
            YANGTZE_PER = 100
        YAVG_BUFF.append(YANGTZE_PER)
        YMAG_AVG = sum(list(YAVG_BUFF))/len(list(YAVG_BUFF))

        #Show averages on color gradient
        KATANA.color_gradient_rg(IMAG_AVG)
    # Shutdown neopixel rings
    KATANA.neopixel_shutdown(MAGENTA)
