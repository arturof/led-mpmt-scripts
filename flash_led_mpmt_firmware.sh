#!/bin/bash
# two comments (Razvan)
# the echo command can be run from any directory, no need to cd into /lib/firmware
# we should change the firmware name to samething that has LED-mPMT in the main, LED-FEB is the light emitter

# previously used commands
#echo LED-mPMT-firmware-v3-25-09-24.bit.bin > /sys/class/fpga_manager/fpga0/firmware
#echo "10MHz-trig-aux-out.bin" > /sys/class/fpga_manager/fpga0/firmware
#echo LED-mPMT-firmware-v3-25-10-09.bit.bin > /sys/class/fpga_manager/fpga0/firmware
#echo LED-mPMT-firmware-v3-25-10-23.bit.bin > /sys/class/fpga_manager/fpga0/firmware
#echo LED-mPMT-firmware-v3-25-10-30.bit.bin > /sys/class/fpga_manager/fpga0/firmware

# current version
echo LED-mPMT-firmware-v3-25-12-04.bit.bin > /sys/class/fpga_manager/fpga0/firmware
rmmod dma-proxy
modprobe dma-proxy
dmesg | tail -n 6
