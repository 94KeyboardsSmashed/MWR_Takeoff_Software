#!/bin/bash
# sudo nice -20 python startup.py && python3 vdd.py > logvdd.txt & python3 gnd.py > loggnd.txt
# sudo nice -20 echo beep && echo ree & echo tee 
# echo ree && echo ree > logvdd.txt & echo tee > loggnd.txt
if echo Working...
then python3 vdd.py > logvdd.txt & python3 gnd.py > loggnd.txt 
else false
fi