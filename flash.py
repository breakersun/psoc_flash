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
    return parser.parse_args()


class FlasherWithBackup(PSocFlashController):
    def __init__(self, product_id=None):
        super().__init__()
        if product_id == 'ccg5':
            self.backup_row_start = 0x13
            self.backup_row_end = 0x53
            self.acquire_mode = 'Reset'
        elif product_id == 'ccg3pa':
            self.backup_row_start = 0x1E9
            self.backup_row_end = 0x1FF
            self.acquire_mode = 'Power'
        else:
            raise ValueError(f'Unknown product id: {product_id}')
        self.records = {}

    def pre_steps(self):
        if self.backup_row_start is None or self.backup_row_end is None:
            return
        for row in track(range(self.backup_row_start, self.backup_row_end + 1),
                         description='Backing up rows'):
            self.records[row] = self.backup_row(row)

    def post_steps(self):
        if self.backup_row_start is None or self.backup_row_end is None:
            return
        for row, record in track(self.records.items(), description='Restoring rows'):
            self.restore_row(row, record)

    def flash_helper(self, hex_file):
        self.open_port()
        self.init_port()
        self.apply_hexfile(hex_file, self.acquire_mode)
        self.pre_steps()
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
    flasher.flash_helper(args.file_path.resolve())
