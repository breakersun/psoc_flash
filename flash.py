import argparse
import pathlib
from psoc_flash_controller import PSocFlashController
from rich.progress import track


def parse_args():
    parser = argparse.ArgumentParser(description='Flash a .hex file to a device')
    parser.add_argument('file_path', type=pathlib.Path, help='path to hex file')
    return parser.parse_args()


class FlasherWithBackup(PSocFlashController):
    def __init__(self, backup_row_start=None, backup_row_end=None):
        super().__init__()
        self.backup_row_start = backup_row_start
        self.backup_row_end = backup_row_end
        if self.backup_row_start is not None \
                and self.backup_row_end is not None:
            assert (self.backup_row_start < self.backup_row_end)
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
        self.apply_hexfile(hex_file)
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

    flasher = FlasherWithBackup(0x13, 0x53)
    flasher.flash_helper(args.file_path.resolve())
