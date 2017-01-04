import png
from PIL import Image
from bitarray import bitarray

INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3.0.png"

image = png.Reader(INPUT_FILE_PATH)

image_width = image.size[0]
image_height = image.size[1]


print("Start decoding")
ba = bitarray()
x = 0
y = 0
zeros_in_a_row = 0
while y < image_height:
    while x < image_width:
        pixel = pixels[x,y]
        hex_string = hex(pixel[3])[2:].zfill(2) + hex(pixel[2])[2:].zfill(2) + hex(pixel[1])[2:].zfill(2) + hex(pixel[0])[2:].zfill(2)
        number = "{0:b}".format(int(hex_string, 16)).zfill(32)
        for bit in number:
            bit = bool(int(bit))
            ba.append(bit)
            if bit:
                zeros_in_a_row = 0
            else:
                zeros_in_a_row += 1

        x += 1
    x = 0
    y += 1

print("Remove unnessary zeros")
while zeros_in_a_row > 0:
    ba.pop()
    zeros_in_a_row -= 1
'''
number = ba.to01().rstrip('0')
ba = bitarray()
for bit in number:
    ba.append(bool(int(bit)))
'''

with open(INPUT_FILE_PATH+".mp3", 'wb') as fh:
    ba.tofile(fh)
print("Finished")