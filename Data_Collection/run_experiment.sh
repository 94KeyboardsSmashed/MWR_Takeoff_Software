#!/bin/bash
# python startup.py && nice -20 python vdd.py > logvdd.txt & python gnd > loggnd.txt
# echo ree && echo ree > logvdd.txt & echo tee > loggnd.txt
# sudo nice -20 python startup.py && python3 vdd.py > logvdd.txt & python3 gnd.py > loggnd.txt
# sudo nice -20 echo beep && echo ree & echo tee 
# echo ree && echo ree > logvdd.txt & echo tee > loggnd.txt

if python3 startup.py 
then python3 vdd.py > logvdd.txt & python3 gnd.py > loggnd.txt 
else false
fi