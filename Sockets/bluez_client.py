"""
A simple Python script to send messages to a sever over Bluetooth
using PyBluez (with Python 2).
"""

import sys
import time
import bluetooth

if __name__ == "__main__":
    serverMACAddress = 'B8:27:EB:81:20:92'
    port = 3
    s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    s.connect((serverMACAddress, port))

    while True:
        for line in sys.stdin:
            text = line
            if text == "# Memory Stop":
                break
            s.send(text)
    s.close()
