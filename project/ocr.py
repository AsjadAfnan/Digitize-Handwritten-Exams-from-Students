import pytesseract
from PIL import Image

def extract_text(image):
    config = r'--oem 3 --psm 6 -l deu'
    return pytesseract.image_to_string(image, config=config)