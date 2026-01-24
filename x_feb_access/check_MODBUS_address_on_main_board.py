# Version 0.1 - R. Gornea on October 24 - fixed hardcoded and wrong slave MODBUS address

from x_feb import xFEB_Modbus
from x_feb import MODBUS_SLAVE_ID
from reg_map import Basic_RW
import sys
import time

my_run_ctr = Basic_RW()
my_device = xFEB_Modbus()

my_run_ctr.WriteReg(1, 0x7ffff)
time.sleep(1)

for led_feb_num in range(0,1):

  #led_feb_address = (my_run_ctr.ReadReg(102) >> 5*led_feb_num) & 0x1f
  #my_run_ctr.WriteReg(1, 1 << led_feb_address)
  #print(f"Power on channel {led_feb_address}")

  for address in range(20,26):
    #try:
    #  read_address = my_device.get_register(address,MODBUS_SLAVE_ID)
    #  print(f"Found LED-FEB {led_feb_address} with MODBUS address {read_address}")
    #except:
    #  pass
    print(f"Found MODBUS address {my_device.get_register(address,MODBUS_SLAVE_ID)}")
    

my_run_ctr.WriteReg(1,0) 

del my_device
del my_run_ctr
