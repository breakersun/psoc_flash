import argparse
import pathlib
from psoc_flash_controller import PSocFlashController
from rich.progress import track
import json


class MetaInfo:
    def __init__(self):
        self.version = None

    def get_version(self):
        with open('info.meta') as info_text:
            version_data = json.load(info_text)
            self.version = version_data.get('FullSemVer')
        return self.version


def parse_args():
    parser = argparse.ArgumentParser(description='Flash a .hex file to a device')
    parser.add_argument('product_id', help='Product ID of the device, now supported: ccg3pa, ccg5')
    parser.add_argument('file_path', type=pathlib.Path, help='path to hex file')
    meta_info = MetaInfo()
    parser.add_argument('--version', action='version',
                        version=f'{meta_info.get_version()}')
    parser.add_argument('--atmode', action='store_true', help=' If this parameter exists, re-enter at mode')
    return parser.parse_args()


class FlasherWithBackup(PSocFlashController):
    def __init__(self, product_id=None):
        super().__init__()
        if product_id == 'ccg5':
            self.backup_row_start = 0x1f7
            self.backup_row_end = 0x1fa
            self.acquire_mode = 'Reset'
        elif product_id == 'ccg3pa':
            self.backup_row_start = 0x1E9
            self.backup_row_end = 0x1FF
            self.acquire_mode = 'Power'
        else:
            raise ValueError(f'Unknown product id: {product_id}')
        self.records = {}

    def _mem_calculate_byte_checksum(self, records, size):
        checksum = 0
        for index in range(size):
            checksum += records[index]
        return (1 + (~checksum)) & 0xFF

    def _enable_atmode(self, records):
        records[0] = 0
        records[1] = 0
        records[2] = 0
        records[3] = 0
        checksum = self._mem_calculate_byte_checksum(records, len(records) - 1)
        records[255] = checksum
        return

    def pre_steps(self, atmode=False):
        if self.backup_row_start is None or self.backup_row_end is None:
            return
        for row in track(range(self.backup_row_start, self.backup_row_end + 1),
                         description='Backing up rows'):
            self.records[row] = self.backup_row(row)

        if atmode:
            self._enable_atmode(self.records[self.backup_row_start])
            self._enable_atmode(self.records[self.backup_row_start + 1])
            
    def post_steps(self):
        if self.backup_row_start is None or self.backup_row_end is None:
            return
        for row, record in track(self.records.items(), description='Restoring rows'):
            self.restore_row(row, record)

    def flash_helper(self, hex_file, atmode=False):
        self.open_port()
        self.init_port()
        self.apply_hexfile(hex_file, self.acquire_mode)
        self.pre_steps(atmode)
        self.erase_chip()
        self.get_rows_count()
        self.pre_checksum()
        self.program_flash()
        self.verify_flash()
        self.post_checksum()
        self.post_steps()
        self.power_off()
        self.close_port()


if __name__ == '__main__':
    args = parse_args()
    flasher = FlasherWithBackup(args.product_id)
    flasher.flash_helper(args.file_path.resolve(), args.atmode)
