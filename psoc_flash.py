import win32com.client
import array
import PPCOM
from PPCOM import enumInterfaces, enumFrequencies, enumSonosArrays


class PortsError(RuntimeError):
    pass


def succeed(hr):
    return hr >= 0


class PSocFlashController(object):
    def __init__(self):
        self.programmer = win32com.client.Dispatch("PSoCProgrammerCOM.PSoCProgrammerCOM_Object")

    def open_port(self):
        (result, ports, last_result) = self.programmer.GetPorts()
        if not succeed(result):
            raise PortsError("Could not get any ports")

        for port in ports:
            if port.startswith("MiniProg4"):
                (result, last_result) = self.programmer.OpenPort(port)
                if succeed(result):
                    return
                else:
                    raise PortsError("Could not open MiniProg4 port")
            raise PortsError("Could not find MiniProg4 port")

    def close_port(self):
        (result, last_result) = self.programmer.ClosePort()
        if not succeed(result):
            raise PortsError("Could not close port")


if __name__ == "__main__":
    p = PSocFlashController()
    p.open_port()
    p.close_port()
