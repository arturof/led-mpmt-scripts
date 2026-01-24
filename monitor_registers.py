#!/usr/bin/env python3
# coding=utf-8

import sys
import time
import datetime
sys.path.append('/root/x_feb_access_Mach_III_October_24_2025')
from reg_map import Basic_RW

# open access to the memory mapped registers
my_run_ctr = Basic_RW()
time.sleep(2)

# list of registers to show
regs = [0, 1]
#regs.extend(list(range(45,85)))
#regs.extend(list(range(2,64)))
regs.extend(list(range(2,104)))

# infinite loop
# stop with ctrl-c
try:
  while True:
    print(datetime.datetime.now())
    for r in regs:
      reg_value = my_run_ctr.ReadReg(r)
      print(f"Register {r:03d}: {reg_value:032b} {reg_value:#010x} {reg_value}")
    print("")
    time.sleep(5)

except KeyboardInterrupt:
  pass
