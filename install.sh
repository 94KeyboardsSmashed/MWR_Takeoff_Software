#!/bin/bash
sudo apt-get update

# Install accel dependancies
sudo apt-get install python-smbus
sudo apt-get install python3-smbus
sudo pip install RPi.GPIO
sudo pip install cap1xxx

#Bluetooth
sudo apt-get install libbluetooth-dev
sudo pip3 install PyBluez

# Install neopixel depenancies
sudo apt-get install build-essential 
sudo apt-get install python-dev 
sudo apt-get install git 
sudo apt-get install scons
sudo apt-get install swig
git clone https://github.com/jgarff/rpi_ws281x.git
cd ./rpi_ws281x
scons
cd ./python
sudo python3 setup.py install
