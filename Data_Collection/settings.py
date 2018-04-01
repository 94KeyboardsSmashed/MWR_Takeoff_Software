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

##Accelerometer Settings:
#: Max Capacity for circular buffer memory
MAXLEN = 2700

#: Output readings in Gs, set to false if measurments in m/s**2 is desired
GFORCE = True

#: Amount of acceleration smoothing needed
ACCEL_RESPONSE = 10

#: Amount of Gs needed to register vehicle liftoff
TAKEOFF_THRESHOLD = 7

#: Amount of G deviation from zero that counts the vehicle as 'landed'
LANDING_THRESHOLD = 0

#: Amount subtracted from landing count when bumped. Set negative number to reset from 0
LANDING_SENSE = -1

#Number of consecutive lines needed
#: below the Landing Threshold for the accelerometer to stop recording
RESTING_THRESHOLD = 2500

#: Max amount of memory available for each file in bytes
MEM_MAX = 5000000

#: XYZ calibration values
CAL_X = 0
CAL_Y = 0 
CAL_Z = 0

# Buzzer BCM channel
CHANNEL = 23

GND_FILE = 'loggnd.txt'
VDD_FILE = 'logvdd.txt'

SERVER_MAC = 'B8:27:EB:99:9D:8A' #'B8:27:EB:81:20:92'
BLUE_PORT = 3
