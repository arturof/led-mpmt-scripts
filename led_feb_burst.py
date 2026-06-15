#!/usr/bin/env python3
# coding=utf-8

import sys
import time
import argparse

sys.path.append('/root/led-mpmt-scripts/x_feb_access')
from reg_map import Basic_RW
from x_feb import xFEB_Modbus

# parse input parameters
parser = argparse.ArgumentParser(description="LED-mPMT flasher")
parser.add_argument("--led_feb_num", type=int, default=0, help="LED-FEB number: 0, 1, 2, 3, 4")
parser.add_argument("--led_num", type=int, default=0, help="LED number (0=c470, 1=c405, 2=c365, 3=c295, 4=d470, 5=d405, 6=d365, 7=all)")
parser.add_argument("--led_bias", type=float, default=2, help="LED bias voltage (min: 2.02V max: 15.28V)")
parser.add_argument("--burst_s", type=int, default=5, help="start time in seconds from current time")
parser.add_argument("--burst_4ns", type=int, default=0, help="start time 4ns component")
parser.add_argument("--flash_n", type=int, default=100000, help="number of flashes in a LED burst")
parser.add_argument("--flash_i", type=int, default=10, help="time between flashes in us (min: 1us)")
args = parser.parse_args()

# burst settings
led_feb_num = args.led_feb_num
led_num     = args.led_num
led_bias    = args.led_bias
burst_s     = args.burst_s
burst_4ns   = args.burst_4ns
flash_n     = int(args.flash_n)
flash_i     = int(args.flash_i*250)

print(f"LED-FEB {led_feb_num} LED {led_num} will be set to start in {burst_s}s+{burst_4ns*4}ns")

# get PMT and LED channel masks
my_run_ctr = Basic_RW()
ispmt_mask = my_run_ctr.ReadReg(103)
isled_mask = ~ispmt_mask & 0x7ffff
#print(f'ispmt             {ispmt_mask:019b}')
#print(f'isled             {isled_mask:019b}')
if (ispmt_mask == 0x7ffff) :
  print('No LED-FEB in firmware')
  sys.exit(1)

# power disable (reg 1) all LED-FEBs
# and deactivate (reg 0) all LED-FEBs to not go in boot mode later
# do not change any PMT
print('Power disabling all LED-FEBs')
reg1 = my_run_ctr.ReadReg(1) & ispmt_mask
reg0 = my_run_ctr.ReadReg(0) & ispmt_mask
my_run_ctr.WriteReg(1, reg1)
my_run_ctr.WriteReg(0, reg0)
#print(f'Register 0        {my_run_ctr.ReadReg(0):019b}')
#print(f'Register 1        {my_run_ctr.ReadReg(1):019b}')
time.sleep(1)

# power enable (reg 1) all LED-FEBs
# activate (reg 0) only one LED-FEB
# do it like this for x_feb to work properly
# do not change any PMT
print(f'Power enabling all LED-FEBs and activating LED-FEB  {led_feb_num}')
reg1 = my_run_ctr.ReadReg(1) | isled_mask
my_run_ctr.WriteReg(1, reg1)
time.sleep(1)

led_feb_address = (my_run_ctr.ReadReg(102) >> 5*led_feb_num) & 0x1f
reg0 = my_run_ctr.ReadReg(0)
my_run_ctr.WriteReg(0, reg0 | 1 << led_feb_address)
print(f'Activated LED-FEB address {led_feb_address}')
#print(f'Register 0        {my_run_ctr.ReadReg(0):019b}')
#print(f'Register 1        {my_run_ctr.ReadReg(1):019b}')
time.sleep(1)

# power on and configure LED-FEB
my_device = xFEB_Modbus()
my_n_led_febs = my_device.get_n_led_febs()
print(f'Number of power enabled LED-FEBs: {my_n_led_febs}')
# all 5 LED-FEBs have to be enabled for x_feb to work properly
# otherwise quit here
if (my_n_led_febs != 5) :
  sys.exit(1)
led_feb_id = led_feb_num

print(f'Powering LED-FEB {led_feb_id}')
while (my_device.power_on(led_feb_id)==False) :
  print('Waiting for power_on')
  time.sleep(1)
print(f'LED-FEB MODBUS address: {my_device.get_led_feb_addr(led_feb_id)}')
print(f'LED-FEB {my_device.fetch_firmware_id(led_feb_id)}')

my_device.set_main_board_trig(led_feb_id)
my_device.trig_enable(led_feb_id)
my_device.led_bias_enable(led_feb_id)
my_device.set_led_bias(led_feb_id,led_bias)

print(f'DAC level: {my_device.get_led_bias(led_feb_id)}')
print(my_device.fetch_trig_source(led_feb_id))
print(my_device.fetch_led_bias(led_feb_id))
print(my_device.fetch_i_mon(led_feb_id))

print(f'Enable LED: {led_num}')
if led_num==0: my_device.enable_channel_0(led_feb_id)
if led_num==1: my_device.enable_channel_1(led_feb_id)
if led_num==2: my_device.enable_channel_2(led_feb_id)
if led_num==3: my_device.enable_channel_3(led_feb_id)
if led_num==4: my_device.enable_channel_4(led_feb_id)
if led_num==5: my_device.enable_channel_5(led_feb_id)
if led_num==6: my_device.enable_channel_6(led_feb_id)
if led_num==7: my_device.enable_all_channels(led_feb_id)

# *********************************************
# Talking to the LED-FEB for configuration here
# *********************************************

# write burst parameters to registers
current_time = my_run_ctr.ReadReg(45)
my_run_ctr.WriteReg(65 + led_feb_num, current_time + burst_s)
my_run_ctr.WriteReg(70 + led_feb_num, burst_4ns)
my_run_ctr.WriteReg(75 + led_feb_num, flash_i)
my_run_ctr.WriteReg(80 + led_feb_num, flash_n)

# read burst parameters from registers
burst_s_read   = my_run_ctr.ReadReg(65 + led_feb_num)
burst_4ns_read = my_run_ctr.ReadReg(70 + led_feb_num)
flash_i_read   = my_run_ctr.ReadReg(75 + led_feb_num)
flash_n_read   = my_run_ctr.ReadReg(80 + led_feb_num)

# print burst parameters
print(f"burst timestamp     = {burst_s_read}")
print(f"burst timestamp 4ns = {burst_4ns_read}")
print(f"flash interval      = {4*flash_i_read/1e3}us")
print(f"number of flashes   = {flash_n_read:e}")

# just clear any previous command if any
my_run_ctr.WriteReg(101, 0x2 << (2*led_feb_num))

# write key to start LED-FEB FSM  and check status
status = (my_run_ctr.ReadReg(100) >> (2*led_feb_num)) & 0x3
print(f"Status = {status}")
key = my_run_ctr.ReadReg(90 + led_feb_num)
print(f"Writing key = {key}")
my_run_ctr.WriteReg(95 + led_feb_num, key)
time.sleep(1) # seems that it is needed for status to update?
status = (my_run_ctr.ReadReg(100) >> (2*led_feb_num)) & 0x3
print(f"Status = {status}")

# monitor FSM
time_now = my_run_ctr.ReadReg(45)
print(f"Initial time = {time_now}")
time_end = (burst_s_read+flash_n_read*flash_i_read*4e-9)+5
print(f"Wait until =   {int(time_end)}")
while (status != 0x0 and time_now<=time_end) :

  # check timestamp and status
  #if status == 0x1 :
  #  print("Waiting on timestamp or burst in progress")
  #elif status == 0x2 :
  if status == 0x2 :
    print("Error")
    my_run_ctr.WriteReg(101, (0x2 << (2*led_feb_num))) # clear error

  # update for next iteration
  time.sleep(1)
  status = (my_run_ctr.ReadReg(100) >> (2*led_feb_num)) & 0x3
  time_now = my_run_ctr.ReadReg(45)
  #print(f"Current time = {time_now}")

time_now = my_run_ctr.ReadReg(45)
print(f"Finished with status = {status}")
print(f"Final time =   {time_now}")

# power off LED-FEB
print(f"Powering off LED-FEB {led_feb_address}")
my_device.led_bias_disable(led_feb_id)
my_device.trig_disable(led_feb_id)
my_device.disable_all_channels(led_feb_id)
my_device.power_off(led_feb_id)
del my_device

# disable LED-FEB
reg0 = my_run_ctr.ReadReg(0) & ispmt_mask
reg1 = my_run_ctr.ReadReg(1) & ispmt_mask
my_run_ctr.WriteReg(0, reg0)
my_run_ctr.WriteReg(1, reg1)
#print(f'Register 0        {my_run_ctr.ReadReg(0):019b}')
#print(f'Register 1        {my_run_ctr.ReadReg(1):019b}')
