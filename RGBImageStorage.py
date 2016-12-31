import os
from time import sleep

import array

from PIL import Image
from bitarray import bitarray

'''
COLOR_CODE_DATA = {
    '[True, True, True]': (256, 256, 256), # Weiss
    '[False, False, True]': (256, 0, 0), # Rot
    '[False, True, False]': (256, 256, 0), # Gelb
    '[False, True, True]': (0, 256, 0), # Gruen
    '[True, False, False]': (0, 256, 256), # Cyan
    '[True, False, True]': (0, 0, 256), # Blau
    '[True, True, False]': (256, 0, 256), # Magenta
    '[False, False, False]': (0, 0, 0), # Schwarz
}
'''
'''
color_code_data = {}
color = 0
color_max = 16777216
while color < 16777216:
    rgb = hex(color)[2:].zfill(6)
    color_code_data[color] = (rgb[4:6], rgb[2:4], rgb[0:2])
    color += 1
'''

COLOR_CODE_NON_DATA = (256, 256, 256) # Grau
COLOR_CODE_SIZE = 24
MAX_IMAGE_WIDTH = 4928
MAX_IMAGE_HEIGHT = 3264

INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3"

size = os.path.getsize(INPUT_FILE_PATH) * 8
file = open(INPUT_FILE_PATH, 'rb')
progress_counter = 0

image = Image.new('RGB', (MAX_IMAGE_WIDTH, MAX_IMAGE_HEIGHT), COLOR_CODE_NON_DATA)
pixels = image.load()


x = 0
y = 0
bit_counter = 0
bits = []

ba = bitarray()
ba.fromfile(file)
for bit in ba:
    bits.append(bit)
    if len(bits) == COLOR_CODE_SIZE:
        progress_counter += COLOR_CODE_SIZE
        if progress_counter % (COLOR_CODE_SIZE*65536) == 0:
            print("{0}".format(1.0*progress_counter / size * 64))
        number = int(''.join('1' if i else '0' for i in bits), 2)
        rgb = hex(number)[2:].zfill(6)
        pixels[x, y] = (int(rgb[4:6], 16), int(rgb[2:4],16), int(rgb[0:2],16))
        bits = []
        x += 1
        if x == MAX_IMAGE_WIDTH:
            y += 1
            x = 0
image.save('image.png')
print("Finished")