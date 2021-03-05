try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

def image2text(image):
    return pytesseract.image_to_string(Image.open(image))