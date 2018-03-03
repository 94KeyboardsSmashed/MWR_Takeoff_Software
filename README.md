<<<<<<< HEAD
# Project Gershwin
## Madison West Rocketry Team Hurgus Payload Coding
=======
<h1 align="center">
  <br>
  <a href="http://liquid.westrocketry.com/index.html"><img src="http://liquid.westrocketry.com/images/patch.png" alt="Madison West Rocketry" width="200"></a>
  <br>
  SLI 2018 Liquid Vibrations
  <br>
</h1>

<h4 align="center">The software running on the payload of Madison West Rocketry's 2018 <a href="https://www.nasa.gov/audience/forstudents/studentlaunch/home/index.html" target="_blank">SLI project</a>.</h4>

# Madison West Rocketry (MWR)
Madison West Rocketry is a group of students who are studying the dampening effects of liquid vibrations in rockets. This repo is for the coding and keyboardsmashing that is needed to get useful data from the project and have a great student launch this year.
>>>>>>> 87196c97fa7a9f86bf9ea9ba695c04e6f9eeb76c

## Project Description
Welcome to our repository.This is the software for our
rocket payload experiment titled "Study of Damping Efficiency in Various Liquids." Considerable
effort was made to keep only the nessesary files for this repository. For any test files and examples
please go to [SLI2017_Hurgus_Madison](https://github.com/94KeyboardsSmashed/SLI2017_Hurgus_Madison).

### Project Gershwin:
- (G)reat
- (E)xperimental
- (R)ocket
- (S)hipment
- (H)ull
- (W)ith view to measure
- l(I)quid
- vibratio(N)s

## Prerequisites
In order to install the dependancies for this program do (sh install.sh). If problems arise, manually install
the following dependancies

### Accelerometer Dependancies
- python-smbus
- python3-smbus
- RPi.GPIO
- cap1xxx

### Bluetooth Dependancies
- PyBluez

### Neopixel Depenancies
- build-essential 
- python-dev 
- git 
- scons
- swig
- The rpi\_ws281x repo (https://github.com/jgarff/rpi_ws281x.git)

## Data Collection
The files in the data collection are the ones that will be used to read accelerometer readout from the payload
sensors. Files include a revamped portion of the rpi_ws281x library to control neopixel rings, and a accelerometer
readout library that interprets the accelerometers that will be attached in an i2c interface. The files VDD.py 
and GND.py will be used to initiate the payload experiment and the readout will be put onto log.txt files. 
### To run the whole setup 
```
sudo sh run_experiment.sh
```
### To run individual files
```
sudo python3 vdd.py
```
or
```
sudo python3 gnd.py
```
### To run individual files and write to log
```
sudo python3 gnd.py > loggnd.txt
```
or
```
sudo python3 vdd.py > logvdd.txt
```
### More than two files can be run and logged like this:
```
sudo nice -20 python3 gnd.py > loggnd.txt & python3 vdd.py > logvdd.txt
```

## Sockets
These are the bluetooth socket programs that we will use to transfer data between the pi's. Currently under
construction.

## License
This software and all associated files are under the MIT license.

## To do
- Integrate bluetooth into data collection?
- Ensure that raspberry pis sync to online time when connected to internet (bash script?)
- Ensure that all raspberry pis start recording when one accelerometer detects launch (or 2 or 3?)
- Create an easy way to switch the pis from lanch mode to rocket fair mode
- Test hardware for heat
- Test hardware for stress
<<<<<<< HEAD
=======

## Other MWR repos
- [MWR_Web](https://github.com/googites/MWR_Web-/blob/master/README.md)
- [SLI2017_Hurgus_Madison](https://github.com/94KeyboardsSmashed/SLI2017_Hurgus_Madison)
- [MWR_PlasmaThruster](https://github.com/googites/MWR_PlasmaThuster)

## Authors
- Benton Likos
- Hyun-seok Chang


