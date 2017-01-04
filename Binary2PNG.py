import os
import struct
from time import sleep

import png
from bitarray import bitarray

COLOR_CODE_NON_DATA = (0, 0, 0, 0) # Schwarz
COLOR_CODE_SIZE = 32
MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 1200

INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3"

size = os.path.getsize(INPUT_FILE_PATH) * 8

print("Image capacity use of {0}%".format((1.0 * size / COLOR_CODE_SIZE) / (MAX_IMAGE_WIDTH * MAX_IMAGE_HEIGHT) * 100))


file = open(INPUT_FILE_PATH, 'rb')
progress_counter = 0


x = 0
y = 0
bit_counter = 0
bits = []
image_counter = 0

def get_int_value(data, index):
    if index >= len(data):
        return 0
    else:
        return struct.unpack('B', data[index + 0])[0]

def get_rgba(data, index):
    red = get_int_value(data, index + 0)
    green = get_int_value(data, index + 1)
    blue = get_int_value(data, index + 2)
    alpha = get_int_value(data, index + 3)
    return (red, green, blue, alpha)

print("Start processing")
rgba_array = list()
row_array = list()

BLOCK_SIZE = 2048
byte_counter = 0
file = open(INPUT_FILE_PATH, 'rb')
while True:
    data = file.read(BLOCK_SIZE)
    if not data:
        break

    byte_counter = 0
    while BLOCK_SIZE > byte_counter:
        row_array.append(get_rgba(data, byte_counter))
        byte_counter += COLOR_CODE_SIZE / 8

        progress_counter += COLOR_CODE_SIZE
        if progress_counter % (COLOR_CODE_SIZE * 65536) == 0:
            print("{0}%".format(1.0 * progress_counter / size * 100))
        x += 1
        if x == MAX_IMAGE_WIDTH:
            rgba_array.append(row_array)
            row_array = list()
            y += 1
            x = 0
        if y == MAX_IMAGE_HEIGHT:
            image = png.from_array(rgba_array, 'RGBA')
            image.save((INPUT_FILE_PATH + ".{0}.png").format(image_counter))
            rgba_array = list()
            row_array = list()
            x = 0
            y = 0
            image_counter += 1

i = len(row_array)
while i < MAX_IMAGE_WIDTH:
    i += 1
    row_array.append((0,0,0,0))

rgba_array.append(row_array)
image = png.from_array(rgba_array, 'RGBA')
image.save((INPUT_FILE_PATH + ".{0}.png").format(image_counter))
print("Finished")


# ES FEHLT DIE PIXEL AUFFUELLUNG