import os
from time import sleep

import array

from PIL import Image
from bitarray import bitarray

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
COLOR_CODE_NON_DATA = (80, 80, 80) # Grau
COLOR_CODE_SIZE = 3
MAX_IMAGE_WIDTH = 4928*2
MAX_IMAGE_HEIGHT = 3264*2

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
            print("{0}".format(1.0*progress_counter / size * 100))
        pixels[x, y] = COLOR_CODE_DATA.get(bits.__str__(), "ERROR")
        bits = []
        x += 1
        if x == MAX_IMAGE_WIDTH:
            y += 1
            x = 0
image.save('image.png')
print("Finished")