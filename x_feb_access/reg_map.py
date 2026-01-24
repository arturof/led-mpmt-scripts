import sys
import mmap

class Basic_RW:
    def __init__(self, fileName = "/dev/uio0", fileMode = "r+b"):
        self.fName = fileName
        self.fMode = fileMode
        self.fID = self.OpenMemoryMapFile()
        self.regs = mmap.mmap(self.fID.fileno(), 0x10000)
    
    def OpenMemoryMapFile(self):
        try:
            return open(self.fName, self.fMode, 0)
        except:
            print(f"[ERROR]: Could not open file {self.fName}")
            sys.exit(-1)
    
    def CheckRegisterAddress(self, regAddress):
        if ((regAddress < 0) or (regAddress > 127)):
            return False
        else:
            return True
    
    def ReadReg(self, regAddress):
        if (self.CheckRegisterAddress(regAddress)):
            return int.from_bytes(self.regs[regAddress * 4 : (regAddress * 4) + 4], byteorder = "little")
        else:
            print(f"[WARNING]: Attempt to access register {regAddress} that is out of the valid range")
            return None
    
    def WriteReg(self, regAddress, setValue):
        if (self.CheckRegisterAddress(regAddress)):
            try:
                self.regs[regAddress * 4 : (regAddress * 4) + 4] = int.to_bytes(setValue, 4, byteorder = "little")
            except:
                print(f"[ERROR]: Could not write register, check if register {regAddress} is read only")
        else:
            print(f"[WARNING]: Attempt to access register {regAddress} that is out of the valid range")
    
