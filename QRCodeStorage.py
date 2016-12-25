import multiprocessing
import os
from multiprocessing.pool import Pool
from threading import Thread

import qrcode
from multiprocessing import Process

class FileData:
    def __init__(self, file_name, data):
        self.file = file_name
        self.data = data

    def __getstate__(self):
        """ This is called before pickling. """
        state = self.__dict__.copy()
        return state

    def __setstate__(self, state):
        """ This is called while unpickling. """
        self.__dict__.update(state)


def create_qr_code_file(file_data):
    qr = qrcode.QRCode(
        version=40,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=4,
    )
    qr.add_data(file_data.data)
    qr.make(fit=None)
    img = qr.make_image()
    img.save(file_data.file)
    qr.clear()

def Worker(mpq):
    while True:
        file_data = mpq.get()
        create_qr_code_file(file_data)

if __name__ == '__main__':
    INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3"
    BLOCK_SIZE = 2048


    size = os.path.getsize(INPUT_FILE_PATH)
    file = open(INPUT_FILE_PATH, 'rb')
    block_size_counter = 0
    mpq = multiprocessing.Queue(3);

    the_pool = multiprocessing.Pool(3, Worker,(mpq,))

    while True:
        data = file.read(BLOCK_SIZE)
        if not data:
            break
        block_size_counter += BLOCK_SIZE
        print("{0}".format(block_size_counter / size * 100))
        mpq.put(FileData("test\\test_{0}.png".format(block_size_counter), data))

    the_pool.join()