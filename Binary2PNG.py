import os
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

print("Start processing")
ba = bitarray()
ba.fromfile(file)
rgba_array = list()
row_array = list()

for bit in ba:
    bits.append(bit)
    if len(bits) == COLOR_CODE_SIZE:
        progress_counter += COLOR_CODE_SIZE
        if progress_counter % (COLOR_CODE_SIZE*65536) == 0:
            print("{0}%".format(1.0*progress_counter / size * 100))
        number = int(''.join('1' if i else '0' for i in bits), 2)
        rgb = hex(number)[2:].zfill(8)
        try:
            pixel = (int(rgb[6:8], 16), int(rgb[4:6], 16), int(rgb[2:4],16), int(rgb[0:2],16))
            row_array.append(pixel)
        except:
            raise Exception("{0}|{1}".format(x, y))
        bits = []
        x += 1
        if x == MAX_IMAGE_WIDTH:
            rgba_array.append(row_array)
            row_array = list()
            y += 1
            x = 0
        if y == MAX_IMAGE_HEIGHT:
            image = png.from_array(rgba_array, 'RGBA')
            image.save((INPUT_FILE_PATH + ".{0}.png").format(image_counter))
            rgba_array  = list()
            row_array = list()
            x = 0
            y = 0
            image_counter += 1
rgba_array.append(row_array)
image = png.from_array(rgba_array, 'RGBA')
image.save((INPUT_FILE_PATH + ".{0}.png").format(image_counter))
print("Finished")


# ES FEHLT DIE PIXEL AUFFUELLUNG