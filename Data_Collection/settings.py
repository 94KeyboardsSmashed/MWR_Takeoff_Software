#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# Python Data Collection Module
#
#
# Created on Wed Jan 31 15:22:27 2018
#
# @author: Hyun-seok
#
# This is the settings file for the data collection modules (gnd.py and vdd.py)
# Any changes here will affect both scripts.
#
#
#
"""
import neopixel_lib as neopxl

##Accelerometer Settings:
#: Max Capacity for circular buffer memory
MAXLEN = 2700

#: Output readings in Gs, set to false if measurments in m/s**2 is desired
GFORCE = False

#: Amount of acceleration smoothing needed
ACCEL_RESPONSE = 10

#: Amount of Gs needed to register vehicle liftoff
TAKEOFF_THRESHOLD = 3

#: Amount of G deviation from zero that counts the vehicle as 'landed'
LANDING_THRESHOLD = 0

#: Amount subtracted from landing count when bumped. Set negative number to reset from 0
LANDING_SENSE = -1

#Number of consecutive lines needed
#: below the Landing Threshold for the accelerometer to stop recording
RESTING_THRESHOLD = 2500

##Neopixel Settings
#: Amount of time needed in testing stage (seconds)
TEST_LENGTH = 10

#: Neopixel Ring Hardware Constants Set 1
LED_COUNT_1 = 24
LED_PIN_1 = 18
LED_FREQ_HZ_1 = 800000
LED_DMA_1 = 5
LED_BRIGHTNESS_1 = 16
LED_INVERT_1 = False

#: Neopixel Ring Hardware Constants Set 2
LED_COUNT_2 = 24
LED_PIN_2 = 13
LED_FREQ_HZ_2 = 800000
LED_DMA_2 = 5
LED_BRIGHTNESS_2 = 16
LED_INVERT_2 = False

#Color Values
RED = neopxl.color_value(255, 0, 0)
GREEN = neopxl.color_value(0, 255, 0)
BLUE = neopxl.color_value(0, 0, 255)
MAGENTA = neopxl.color_value(255, 0, 255)
