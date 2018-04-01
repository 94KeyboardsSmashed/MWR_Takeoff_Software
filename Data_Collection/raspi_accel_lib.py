# -*- coding: utf-8 -*-
#Python Acceleration Libraries Module

"""
Created on Tue May  9 12:13:27 2017

@author: Hyun-seok

Please use indents as they are incompatible with spaces
and spaces are a pain in the arse to do 5 times for every indent

Accel libraries adapted form ADXL345 Python library for Raspberry Pi by Jonathan Williamson.
"""

import time
import math
import smbus
import RPi.GPIO as GPIO

# select the correct i2c bus for this revision of Raspberry Pi
REVISION = ([l[12:-1] for l in open('/proc/cpuinfo', 'r').readlines() if l[:8] == "Revision"]+['0000'])[0]
BUS = smbus.SMBus(1 if int(REVISION, 16) >= 4 else 0)

# ADXL345 constants
EARTH_GRAVITY_MS2 = 9.80665
SCALE_MULTIPLIER = 0.004

DATA_FORMAT = 0x31
BW_RATE = 0x2C
POWER_CTL = 0x2D

BW_RATE_1600HZ = 0x0F
BW_RATE_800HZ = 0x0E
BW_RATE_400HZ = 0x0D
BW_RATE_200HZ = 0x0C
BW_RATE_100HZ = 0x0B
BW_RATE_50HZ = 0x0A
BW_RATE_25HZ = 0x09

RANGE_2G = 0x00
RANGE_4G = 0x01
RANGE_8G = 0x02
RANGE_16G = 0x03

MEASURE = 0x08
AXES_DATA = 0x32

def buzzer_beep(start_counter, start_time, channel, state=False, ontime=0.1, offtime=2):
    """
    Beeps the beeper based on ontime and offtime

    Parameters
    ----------
    start_counter : float (or int)
        Time between interation at the start
    
    start_time : float (or int)
        Time at the start of the command execution in unix epoch time

    channel : int
        GPIO pin output, BCM
    
    state=False : bool
        State of the buzzer at startup. False is off, True is on.
    
    ontime=0.1 : float (or int)
        Time that the beeper is in its on state
    
    offtime=2 : float (or int)
        Time that the beeper is in its off state

    Returns
    -------
    None
    """
    counter = start_counter
    timer = start_time
    if time.time() - timer > 0.1:
        timer = time.time()
        counter = counter - 0.1
        
    if counter <= 0 and state == False:
        ontime = counter
        state = True
        
    if counter <= 0 and state == True:
        offtime = counter
        state = False

    GPIO.output(channel, state)

class ADXL345:
    """Main Class for everything to do with the ADXL345"""

    address = None

    def __init__(self, calx, caly, calz, address=0x53):
        self.address = address
        self.set_bandwidth_rate(BW_RATE_100HZ)
        self.set_range(RANGE_16G)
        self.enable_measurement()
        self.mag_measurement = 0
        self.cal_x = calx
        self.cal_y = caly
        self.cal_z = calz

    def enable_measurement(self):
        """
        Initiates and enables the measurment of data from the accelerometer

        Runs at class __init__.

        Parameters
        ----------
        self : Part of class ADXL345

        Returns
        -------
        None

        """
        BUS.write_byte_data(self.address, POWER_CTL, MEASURE)

    def set_bandwidth_rate(self, rate_flag):
        """
        Set the measurement range of the accelerometer for 10-bit readings.

        Runs at class __init__.

        Parameters
        ----------
        self : Part of class ADXL345

        Returns
        -------
        None

        """
        BUS.write_byte_data(self.address, BW_RATE, rate_flag)

    def set_range(self, range_flag):
        """
        Original developer notes:
        returns the current reading from the sensor for each axis parameter gforce:
        #    False (default): result is returned in m/s^2
        #    True           : result is returned in gs

        Determines the range values for the accelerometer.

        Runs at class __init__.

        Parameters
        ----------
        self : Part of class ADXL345

        Returns
        -------
        None

        """
        value = BUS.read_byte_data(self.address, DATA_FORMAT)

        value &= ~0x0F;
        value |= range_flag;
        value |= 0x08;

        BUS.write_byte_data(self.address, DATA_FORMAT, value)

    def get_axes(self, gforce=False):
        """
        Returns the measurement of the axes of the accelerometer in a dictionary (x,y,z)

        Parameters
        ----------
        self : Part of class ADXL345

        gforce=False : boolean
            If true, outputs measurement in Gs. Else measures in m/s^2

        Returns
        -------
        dict
            {"x": x measurement, "y": y measurement, "z": z measurement}
        """
        _bytes = BUS.read_i2c_block_data(self.address, AXES_DATA, 6)

        _x = _bytes[0] | (_bytes[1] << 8)
        if _x & (1 << 16 - 1):
            _x = _x - (1<<16)

        _y = _bytes[2] | (_bytes[3] << 8)
        if _y & (1 << 16 - 1):
            _y = _y - (1<<16)

        _z = _bytes[4] | (_bytes[5] << 8)
        if _z & (1 << 16 - 1):
            _z = _z - (1<<16)

        _x = _x * SCALE_MULTIPLIER
        _y = _y * SCALE_MULTIPLIER
        _z = _z * SCALE_MULTIPLIER

        _x += self.cal_x
        _y += self.cal_y
        _z += self.cal_z

        if not gforce:
            _x = _x * EARTH_GRAVITY_MS2
            _y = _y * EARTH_GRAVITY_MS2
            _z = _z * EARTH_GRAVITY_MS2

        _x = round(_x, 4)
        _y = round(_y, 4)
        _z = round(_z, 4)

        return {"x": _x, "y": _y, "z": _z}

    def string_output(self, gees=False):
        """
        Returns a string 'time, x, y, z'

        Use mainly for logging onto .txt files

        Parameters
        ----------
        self : Part of class ADXL345

        gees=False : bool
            If true, outputs measurement in Gs. Else measures in m/s^2

        Returns
        -------
        str
            'time, x measurement, y measurment, z measurement'
        """
        axes = self.get_axes(gees)
        return "{},{},{},{}".format(time.time(), axes['x'], axes['y'], axes['z'])

    def accel_magnitude(self, gees=False):
        """
        Returns acceleration magnitude

        Parameters
        ----------
        self : Part of class ADXL345

        gees=False : bool
            If true, outputs measurement in Gs. Else measures in m/s^2

        Returns
        -------
        float
            If measured in Gs:
                |sqrt(x measurement^2 + y measurement^2 + z measurment^2) - 1|
            If measured in m/s^2:
                |sqrt(x measurement^2 + y measurement^2 + z measurment^2) - 9.81|

        """
        axes = self.get_axes(gees)
        if gees:
            mag = abs(math.sqrt(axes['x']**2 + axes['y']**2 + axes['z']**2)-1)
        else:
            mag = abs(math.sqrt(axes['x']**2 + axes['y']**2 + axes['z']**2)-9.81)
        return mag

    def accel_startup(self, check, gees=False):
        """
        initiates accelerometers and checks for accelerometer measurement anomalies.

        Takes the magnitude measurment from the data from the accelerometer and checks them
        against the check value given by the user.

        Parameters
        ----------
        self : Part of class ADXL345

        check : float (or int)
            The value to check the measurment of the accelerometer against. If measure
            is greater than check raises message.

        gees=False : bool
            If true, outputs measurement in Gs. Else measures in m/s^2

        Returns
        -------
        str
            If measured magnitude > check:
                #Accel Value Startup Mag > check value
            else:
                "#Checked and ready to go"
        """
        mag = self.accel_magnitude(gees)
        if mag > check:
            return "#Accel Value Startup Mag > {}".format(check)
        return "#Checked and ready to go"
