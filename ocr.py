from PIL import Image
import pytesseract

def card_ocr(img_path):
    # try:
    img = Image.open(img_path) 
    # except:
    # pass
    ocr = pytesseract.image_to_string(img, lang='eng')
    return ocr


print("test.png: %s" % card_ocr('test.png'))
print("Tangle.png: %s" % card_ocr('Tangle.jpg'))
print("Tangle.png: %s" % card_ocr('tangle-chop.png'))
