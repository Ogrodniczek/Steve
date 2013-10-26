import os
import datetime
import numpy
import cv2
from ImageBuffer import ScreenBits


class BitmapGrinder(ScreenBits):
    def __init__(self, title):
        ScreenBits.__init__(self, title)

    def find_pattern(self, image, sub=None):
        then = datetime.datetime.now()
        if sub != None:
            np_array = sub
            print('sub')
        else:
            np_array = numpy.asarray(self.im)
        pattern = cv2.imread(image)
        result = cv2.matchTemplate(np_array,pattern,cv2.TM_CCOEFF_NORMED)
        y,x = numpy.unravel_index(result.argmax(), result.shape)

        print ('x: ', x, 'y: ',y)
        print 'searching handle', datetime.datetime.now()-then

    def crop_image(self, x1, x2, y1, y2):
        then = datetime.datetime.now()
        small_array = numpy.asarray(self.im)[y1:y2, x1:x2]
        print 'crop', datetime.datetime.now()-then


if __name__ == "__main__":
    #screen = BitmapGrinder('EVE')
    screen = BitmapGrinder('Computer')
    screen.initialize_window()
    screen.refresh_image()
    screen.find_pattern(os.path.abspath(os.path.join('.', 'favorites'+".bmp")))
    screen.find_pattern(os.path.abspath(os.path.join('.', 'workgroup'+".bmp")))
    #screen.crop_image(15, 140, 72, 306, os.path.abspath(os.path.join('.', 'pictures'+".bmp")))
    screen.save_window_image()