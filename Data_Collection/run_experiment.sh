#!/bin/bash
sudo python startup.py; sudo nice -20 python gnd.py > logGND.txt & python vdd.py > logVDD.txt
