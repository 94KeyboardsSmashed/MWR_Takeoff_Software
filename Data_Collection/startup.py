#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#Python Data Collection Module

"""
Created on Tue May 9 12:13:27 2017

@author: Hyun-seok

IMPORTANT: REQUIRES ROOT ACCESS TO RUN.

Reads and interprets data from an ADXL 345 triaxial accelerometer and uses
a Adafruit 24 pixel neopixel ring to determine payload status. Used at startup
to make the neopixel ring change different colors.

Examples:
Run with the following lines on the command prompt:
    $ sudo python startup.py

Wiring Details:

    Connect neopixel to ground, 5v, and physical pin 12 (gpio pin 18) (0)
    #(not needed) Connect neopixel to ground, 5v, and physical pin 33 (gpio pin 13) (1)

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
    SDO - 3V3
"""
import time
import collections
import raspi_accel_lib
import neopixel_lib as neopxl
import settings as st

if __name__ == '__main__':
    # init global variables
    IAVG_BUFF = collections.deque(maxlen=st.ACCEL_RESPONSE)
    YAVG_BUFF = collections.deque(maxlen=st.ACCEL_RESPONSE)

    # Define accelerometers (named after rivers)
    INDUS = raspi_accel_lib.ADXL345(0x1D)
    YANGTZE = raspi_accel_lib.ADXL345(0x53)

    # Define Neopixels (named after swords)
    KATANA = neopxl.Adafruit_NeoPixel(st.LED_COUNT_1, st.LED_PIN_1, st.LED_FREQ_HZ_1,
                                      st.LED_DMA_1, st.LED_INVERT_1, st.LED_BRIGHTNESS_1, 0)

    # Startup Neopixel
    KATANA.neopixel_startup(st.BLUE, st.GREEN, st.RED)

    # Startup Accelerometer
    INDUS.accel_startup(st.GFORCE)
    YANGTZE.accel_startup(st.GFORCE)

    # Make Indus testable at start
    TEST_TIMER = time.time() + st.TEST_LENGTH

    while time.time() < TEST_TIMER:
        #Process light color by finding averages
        INDUS_PER = INDUS.accel_magnitude()*10
        if INDUS_PER > 100:
            INDUS_PER = 100
        IAVG_BUFF.append(INDUS_PER)
        IMAG_AVG = sum(list(IAVG_BUFF))/len(list(IAVG_BUFF))

        #Show averages on color gradient
        KATANA.color_gradient_rg(IMAG_AVG)

    # Make Yangtze testable second
    KATANA.color_wipe(st.MAGENTA)
    TEST_TIMER = time.time() + st.TEST_LENGTH

    while time.time() < TEST_TIMER:
        #Process light color by finding adverages
        YANGTZE_PER = YANGTZE.accel_magnitude()*10
        if YANGTZE_PER > 100:
            YANGTZE_PER = 100
        YAVG_BUFF.append(YANGTZE_PER)
        YMAG_AVG = sum(list(YAVG_BUFF))/len(list(YAVG_BUFF))

        #Show averages on color gradient
        KATANA.color_gradient_rg(YMAG_AVG)
    # Shutdown neopixel rings
    KATANA.neopixel_shutdown(st.MAGENTA)
