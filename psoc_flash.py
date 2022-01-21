import win32com.client
import array
import PPCOM
from PPCOM import enumInterfaces, enumFrequencies, enumSonosArrays


class PSocFlashController(object):
    def __init__(self):
        self.programmer = win32com.client.Dispatch("PSoCProgrammerCOM.PSoCProgrammerCOM_Object")

    def open_port(self):
        (_, (port, *_), *_) = self.programmer.GetPorts()
        print(port)


if __name__ == "__main__":
    p = PSocFlashController()
    p.open_port()
