import tesseract

class OCRBitmap:
    def __init__(self):
        pass
#os.path.join('.', 'Overview'+".bmp")
import cv2.cv as cv
import cv2
import os

image0=cv2.imread(os.path.join('.', 'Impairor2'+".tif"))
gray = cv2.cvtColor(image0,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(5,5),0)
#small = cv2.resize(image0, (0,0), fx=10, fy=10)
#### you may need to thicken the border in order to make tesseract feel happy to ocr your image #####
offset=10
height,width,channel = image0.shape
#image1=cv2.copyMakeBorder(image0,offset,offset,offset,offset,cv2.BORDER_CONSTANT,value=(255,255,255))
#thresh2 = cv2.adaptiveThreshold(gray,255,1,1,7,5)
#ret,thresh2 = cv2.threshold(image1,60,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(gray,70,255,cv2.THRESH_BINARY)
ret,thresh3 = cv2.threshold(gray,70,255,cv2.THRESH_BINARY)
thresh2 = cv2.cvtColor(thresh2,cv2.COLOR_BAYER_BG2RGB)
contours,hierarchy = cv2.findContours(thresh3,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)

for cnt in contours:
    #print cv2.contourArea(cnt)
    if cv2.contourArea(cnt)>20:
        [x,y,w,h] = cv2.boundingRect(cnt)
        if  h>20:
            cv2.rectangle(thresh2,(x,y),(x+w,y+h),(0,0,255),2)
            roi = thresh2[y:y+h,x:x+w]
            roismall = cv2.resize(roi,(10,10))
            #cv2.imshow('norm', image0)
            #key = cv2.waitKey(0)
cv2.imshow('norm', thresh2)
#cv2.imshow('dst_rt', thresh3)
cv2.waitKey(0)
cv2.destroyAllWindows()
import Image
im = Image.fromarray(thresh2)
im.save("your_file.bmp")
#thresh2.save('whatev', format = 'png')
#cv2.namedWindow("Test")
#cv2.imshow("Test", image1)
#cv2.waitKey(0)
#cv2.destroyWindow("Test")
#####################################################################################################