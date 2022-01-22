import win32com.client
from PPCOM import enumInterfaces, enumFrequencies, enumSonosArrays, enumVoltages
from rich.progress import track


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
        self.row_size = None
        self.rows_count = None
        self.image_size = None
        self.pre_checksum_privileged = None
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

        self.image_size = image_size

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

    def pre_checksum(self):
        (result, pre_checksum_privileged, _) = self.programmer.PSoC4_CheckSum(0x8000)
        if not succeed(result):
            raise DeviceError("Could not pre checksum")
        self.pre_checksum_privileged = pre_checksum_privileged

    def post_checksum(self):
        (result, post_checksum_privileged, _) = self.programmer.PSoC4_CheckSum(0x8000)
        if not succeed(result):
            raise DeviceError("Could not post checksum")
        checksum_user = post_checksum_privileged - self.pre_checksum_privileged

        (result, hex_checksum, _) = self.programmer.HEX_ReadChecksum()
        if not succeed(result):
            raise PlatformError("Could not get checksum from hex file")

        checksum_user = checksum_user & 0xFFFF
        hex_checksum = hex_checksum & 0xFFFF

        if checksum_user != hex_checksum:
            raise PlatformError("Checksum mismatch")

    def get_rows_count(self):
        (result, rows_per_array, row_size, _) = self.programmer.PSoC4_GetFlashInfo()
        if not succeed(result):
            raise DeviceError("Could not get flash info")

        self.rows_count = int(self.image_size / row_size)
        self.row_size = row_size

    def program_flash(self):
        for i in track(range(0, self.rows_count), description="Programming flash..."):
            (result, _) = self.programmer.PSoC4_ProgramRowFromHex(i)
            if not succeed(result):
                raise DeviceError(f"Could not program row {i}")

    def verify_flash(self):
        for i in track(range(0, self.rows_count), description="Verifying flash...  "):
            (result, verified, _) = self.programmer.PSoC4_VerifyRowFromHex(i)
            if not succeed(result):
                raise DeviceError(f"Could not verify row {i}")
            if not verified:
                raise DeviceError(f"Row {i} verification failed")

    def backup_row(self, row_id) -> memoryview:
        (result, readout, _) = self.programmer.PSoC4_ReadRow(row_id)
        if not succeed(result):
            raise DeviceError(f"Could not backup row {row_id}")
        return readout

    def restore_row(self, row_id, row_data: memoryview):
        (result, _) = self.programmer.PSoC4_WriteRow(row_id, row_data)
        if not succeed(result):
            raise DeviceError(f"Could not restore row {row_id}")


# this is some quick test code, don't use it in production
if __name__ == "__main__":
    p = PSocFlashController()
    p.open_port()
    p.init_port()
    p.apply_hexfile("E:\\test_path\fw.hex")
    p.erase_chip()
    p.get_rows_count()
    p.pre_checksum()
    p.program_flash()
    p.verify_flash()
    p.post_checksum()
    backup = p.backup_row(0x00)
    p.restore_row(0x00, backup)
    p.close_port()
