import multiprocessing
import os
from multiprocessing.pool import Pool
from threading import Thread

import qrcode

INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3"
BLOCK_SIZE = 2048


class FileData:
    def __init__(self, file, data):
        self.file = file
        self.data = data


def create_qr_code_file(file_data):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=4,
        border=1,
    )
    qr.add_data(file_data.data)
    qr.make(fit=True)
    img = qr.make_image()
    img.save(file_data.file)
    qr.clear()

size = os.path.getsize(INPUT_FILE_PATH)
file = open(INPUT_FILE_PATH, 'rb')
block_size_counter = 0
pool = Pool(processes=4)

while True:
    data = file.read(BLOCK_SIZE)
    if not data:
        break
    block_size_counter += BLOCK_SIZE
    print("{0}".format(block_size_counter / size * 100))
    pool.starmap(create_qr_code_file(FileData(file, data)))
