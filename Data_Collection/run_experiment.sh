#!/bin/bash

echo Starting Up Project ... 
echo Working...
sudo python3 vdd.py | tee ./Data_Logs/`date +%s`_vdd.txt ../../Backup_Data/`uuidgen`_vdd.txt > logvdd.txt & 
sudo python3 gnd.py | tee ./Data_Logs/`date +%s`_gnd.txt ../../Backup_Data/`uuidgen`_gnd.txt > loggnd.txt 

