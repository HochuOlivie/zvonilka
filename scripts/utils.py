from PIL import Image
import base64
import pytesseract
import io


def phone_b64_parse(b64str):
    imgstring = b64str.split('base64,')[-1].strip()
    pic = io.StringIO()
    image_string = io.BytesIO(base64.b64decode(imgstring))
    image = Image.open(image_string)

    # Overlay on white background, see http://stackoverflow.com/a/7911663/1703216
    bg = Image.new("RGB", image.size, (255, 255, 255))
    bg.paste(image, image)
    return pytesseract.image_to_string(bg)