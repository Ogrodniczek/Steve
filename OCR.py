import tesseract

class OCRBitmap:
    def __init__(self):
        pass
#os.path.join('.', 'Overview'+".bmp")
import cv2.cv as cv
import cv2
import os
import tesseract

api = tesseract.TessBaseAPI()
api.Init('.',"eng",tesseract.OEM_DEFAULT)
api.SetVariable("tessedit_char_whitelist", "0123456789ABCDEFGHIJKLMNOPRSTUWXYZabcdefghijklmnopqrstuvwxyz")
api.SetPageSegMode(tesseract.PSM_AUTO)

image=cv.LoadImage(os.path.join('.', 'Impairor'+".bmp"), cv.CV_LOAD_IMAGE_GRAYSCALE)
tesseract.SetCvImage(image,api)
text=api.GetUTF8Text()
conf=api.MeanTextConf()
print text
print conf
