# Version 0.1 - R. Gornea on October 24 - fixed hardcoded and wrong slave MODBUS address

from x_feb import xFEB_Modbus
from x_feb import MODBUS_SLAVE_ID
import sys

if (len(sys.argv) > 1):
    my_new_modbus_addr = sys.argv[1]
    print(f"Attempting to change the MODBUS address to {my_new_modbus_addr}")
else:
    print("Usage: change_MODBUS_address_on_main_board.py <NEW MODBUS ADDRESS>")
    sys.exit(-1)

my_device = xFEB_Modbus()

my_status = my_device.set_register(20, MODBUS_SLAVE_ID, int(my_new_modbus_addr))
if (my_status == True):
    print("The MODBUS address has been successfully changed")
else:
    print("[WARNING]: Could not change the MODBUS address!")

del my_device
