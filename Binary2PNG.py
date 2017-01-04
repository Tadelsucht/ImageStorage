# Imports
import os
import struct
import math
import png

# Constants
MAX_IMAGE_WIDTH = 1200
MAX_IMAGE_HEIGHT = 1200
INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3"
COLOR_CODE_NON_DATA = (0, 0, 0, 0)  # Black
COLOR_CODE_BITS = 32


# Functions
def get_int_value(data, index):
    if index >= len(data):
        return 0
    else:
        return struct.unpack('B', data[index + 0])[0]


# Program
size = os.path.getsize(INPUT_FILE_PATH) * 8
print("Necessary files {0}".format(int(math.ceil((1.0 * size / COLOR_CODE_BITS) / (MAX_IMAGE_WIDTH * MAX_IMAGE_HEIGHT)))))

file = open(INPUT_FILE_PATH, 'rb')
progress_counter = 0
x = 0
y = 0
bit_counter = 0
bits = []
image_counter = 0
rgba_array = list()
row_array = list()

print("Start processing")
BLOCK_SIZE = 2048
byte_counter = 0
file = open(INPUT_FILE_PATH, 'rb')
while True:
    data = file.read(BLOCK_SIZE)
    if not data:
        break

    byte_counter = 0
    while BLOCK_SIZE > byte_counter:
        row_array.append((get_int_value(data, byte_counter + 0), get_int_value(data, byte_counter + 1),
                          get_int_value(data, byte_counter + 2), get_int_value(data, byte_counter + 3)))
        byte_counter += COLOR_CODE_BITS / 8

        progress_counter += COLOR_CODE_BITS
        if progress_counter % (COLOR_CODE_BITS * 65536) == 0:
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
    row_array.append((0, 0, 0, 0))
print("Write Image")
rgba_array.append(row_array)
image = png.from_array(rgba_array, 'RGBA')
image.save((INPUT_FILE_PATH + ".{0}.png").format(image_counter))
print("Finished")