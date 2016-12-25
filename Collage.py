import os

from PIL import Image

x = 0
y = 0
matrix = 8

img = Image.new('RGB', (370*matrix, 370*matrix))
for file in os.listdir('test'):
    loaded_img = Image.open('test\\{0}'.format(file), 'r')
    offset = 370 * x, 370 * y
    img.paste(loaded_img, offset)
    print("{0}:{1},{2}".format(file,x,y))
    if (x+y) == matrix+matrix-2:
        img.save('image.png')
        img = Image.new('RGB', (370*matrix, 370*matrix))
        break
    if x < matrix-1:
        x += 1
    else:
        x = 0
        y += 1