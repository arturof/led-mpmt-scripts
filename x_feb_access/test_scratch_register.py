# Version 0.1 - R. Gornea on August 8, 2025 - created the first version

import sys
import os
import random
from reg_map import Basic_RW

N_TRIALS = 3
SCRATCH_REG_ADDR_1 = 103
SCRATCH_REG_ADDR_2 = 104

if (os.path.exists("/dev/uio0") == False):
    print("[ERROR]: Could not find memory mapped registers file!")
    sys.exit(-1)
else:
    my_regs = Basic_RW()
    for my_index in range(N_TRIALS):
        print(f" *** Test {my_index} *** ")
        my_scratch_1 = my_regs.ReadReg(SCRATCH_REG_ADDR_1)
        my_scratch_2 = my_regs.ReadReg(SCRATCH_REG_ADDR_2)
        print(f"Initial values of the scratch registers are {my_scratch_1} and {my_scratch_2}")
        my_random_int = random.randint(0, 65535)
        print(f"Writing random integer {my_random_int} to the first scratch register")
        my_regs.WriteReg(SCRATCH_REG_ADDR_1, my_random_int)
        my_scratch_1 = my_regs.ReadReg(SCRATCH_REG_ADDR_1)
        my_scratch_2 = my_regs.ReadReg(SCRATCH_REG_ADDR_2)
        print(f"Values of the scratch registers after writing the first register are {my_scratch_1} and {my_scratch_2}")
        my_random_int = random.randint(0, 65535)
        print(f"Writing random integer {my_random_int} to the second scratch register")
        my_regs.WriteReg(SCRATCH_REG_ADDR_2, my_random_int)
        my_scratch_1 = my_regs.ReadReg(SCRATCH_REG_ADDR_1)
        my_scratch_2 = my_regs.ReadReg(SCRATCH_REG_ADDR_2)
        print(f"Values of the scratch registers after writing the second register are {my_scratch_1} and {my_scratch_2}")
