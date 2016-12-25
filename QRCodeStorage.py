import qrcode

INPUT_FILE_PATH = "LukHash_-_THE_OTHER_SIDE.mp3"
BLOCK_SIZE = 1

qr = qrcode.QRCode(
    version=1,
    error_correction=qrcode.constants.ERROR_CORRECT_L,
    box_size=10,
    border=4,
)

file = open(INPUT_FILE_PATH, 'rb')
block_size_counter = 0
while True:
    data = file.read(BLOCK_SIZE)
    if not data:
        break
    qr.add_data(data)
    block_size_counter += BLOCK_SIZE
    if(block_size_counter / BLOCK_SIZE) > 10:
        qr.make(fit=True)
        img = qr.make_image()
        img.save("test.png")
        qr.clear()



