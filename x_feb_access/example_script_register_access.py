import time
import sys
import os
from reg_map import Basic_RW

if (os.path.exists("/dev/uio0") == True):
    my_run_ctr = Basic_RW() # open access to the memory mapped registers
else:
    print("[WARNING]: Will use the debuging mode with a single board")
    sys.exit(-1)

time.sleep(2)

my_power_status = my_run_ctr.ReadReg(1) # read the power register

print(f"Initial value of the power register is {my_power_status}")

time.sleep(2)

my_run_ctr.WriteReg(1, 1) # write the power register

my_power_status = my_run_ctr.ReadReg(1) # read again the power register

print(f"Value of the power register after turning channel 1 ON is {my_power_status}")

time.sleep(2)

my_run_ctr.WriteReg(1, 0) # write again the power register

my_power_status = my_run_ctr.ReadReg(1) # read again the power register

print(f"Value of the power register after turning channel 1 OFF is {my_power_status}")


