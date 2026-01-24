#!/bin/bash


#source ~/stop_mbusd.sh
#sleep 1

python3 reprogram_LED_FEBs.py --filename x_feb_access/LED_FEB_2.hex --baud 115200 --port /dev/ttyPS1 -n all

#source ~/start_mbusd.sh
