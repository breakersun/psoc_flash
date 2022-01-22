import argparse
import pathlib
from psoc_flash_controller import PSocFlashController
from rich.progress import track


def parse_args():
    parser = argparse.ArgumentParser(description='Flash a .hex file to a device')
    parser.add_argument('file_path', type=pathlib.Path, help='path to hex file')
    return parser.parse_args()


class FlasherWithBackup(PSocFlashController):
    def __init__(self, row_ids=None):
        super().__init__()

        if row_ids is None:
            self.row_ids = [0x00, 0x01]  # default to back up row 00 01 for testing
        else:
            self.row_ids = row_ids
        self.records = {}

    def pre_steps(self):
        for row in track(self.row_ids, description='Backuping rows'):
            self.records[row] = self.backup_row(row)

    def post_steps(self):
        for row in track(self.row_ids, description='Restoring rows'):
            self.restore_row(row, self.records[row])

    def flash_helper(self, hex_file):
        self.open_port()
        self.init_port()
        self.apply_hexfile(hex_file)
        self.pre_steps()
        self.erase_chip()
        self.get_rows_count()
        self.pre_checksum()
        self.program_flash()
        self.verify_flash()
        self.post_checksum()
        self.post_steps()
        self.close_port()


if __name__ == '__main__':
    args = parse_args()

    flasher = FlasherWithBackup()
    flasher.flash_helper(args.file_path)
