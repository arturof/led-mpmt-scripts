#!/bin/bash
echo LED-mPMT-firmware-v3-26-04-17.bin > /sys/class/fpga_manager/fpga0/firmware
rmmod dma-proxy
modprobe dma-proxy
dmesg | tail -n 6
