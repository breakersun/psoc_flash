import win32com.client
from PPCOM import enumInterfaces, enumFrequencies, enumSonosArrays, enumVoltages


class PortsError(RuntimeError):
    pass


class DeviceError(RuntimeError):
    pass


class PlatformError(RuntimeError):
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

    def init_port(self):
        # power on
        self.programmer.SetPowerVoltage("3.3V")
        (result, last_result) = self.programmer.PowerOn()
        print(result)
        if not succeed(result):
            raise DeviceError("Could not power on")

        # set protocol, connector, and frequency
        (result, last_result) = self.programmer.SetProtocol(enumInterfaces.SWD)
        if not succeed(result):
            raise DeviceError("Could not set protocol")
        self.programmer.SetProtocolConnector(1)  # 1 should be 10 pin connector ?
        self.programmer.SetProtocolClock(enumFrequencies.FREQ_01_6)  # came from the UI programmer default settings, idk

    def apply_hexfile(self, hex_file):
        (result, image_size, last_result) = self.programmer.HEX_ReadFile(hex_file)
        if not succeed(result):
            raise PlatformError("Could not load hex file")

        self.programmer.SetAcquireMode("Reset")
        (result, _) = self.programmer.DAP_Acquire()
        if not succeed(result):
            raise DeviceError("Could not acquire")

        (result, chip_id, _) = self.programmer.PSoC4_GetSiliconID()
        if not succeed(result):
            raise DeviceError("Could not get chip id")

        (result, hex_chip_id, _) = self.programmer.HEX_ReadJtagID()
        if not succeed(result):
            raise PlatformError("Could not get chip id from hex file")
        chip_id = bytes(chip_id)
        hex_chip_id = bytes(hex_chip_id)
        for i in range(4):
            if i == 2:
                continue
            if chip_id[i] != hex_chip_id[i]:
                raise PlatformError("Chip id mismatch, wrong file file")

    def erase_chip(self):
        (result, _) = self.programmer.PSoC4_EraseAll()
        if not succeed(result):
            raise DeviceError("Could not erase chip")

if __name__ == "__main__":
    p = PSocFlashController()
    p.open_port()
    p.init_port()
    p.apply_hexfile("E:\\working_case\\Projects_2021\\00_Skeling\\firmware\\fw.hex")
    p.erase_chip()
    p.close_port()
