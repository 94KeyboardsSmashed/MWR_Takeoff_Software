"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import sys
import time
import subprocess
import bluetooth
import settings as st
import RPi.GPIO as GPIO

if __name__ == "__main__":
    serverMACAddress = st.SERVER_MAC
    port = st.BLUE_PORT
    subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
    time.sleep(10)
    try:
        s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        s.connect((serverMACAddress, port))

        with open('loggnd.txt') as lgnd:
            for line in lgnd:
                text = line.strip() + ', gnd'
                s.send(text)
    
        with open('logvdd.txt') as lvdd:
            for line in lvdd:
                text = line.strip() + ', vdd'
                s.send(line)

        s.close()

    except:
        pass

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(st.CHANNEL, GPIO.OUT)

    start = time.time()
    counter = 1
    state = False    
    
    while True:
        if time.time() - start > 0.1:
            start = time.time()
            counter = counter - 0.1
        
        if counter <= 0 and state == False:
            counter = 2
            state = True
        
        if counter <=0 and state == True:
            counter = 5
            state = False

        GPIO.output(st.CHANNEL, state)
        

