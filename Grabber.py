import sys
import win32gui
import win32con
import timeit
import win32ui
import win32api
import os
import random
import Image
import datetime
import numpy
import cv2


class EnumWind:
    def __init__(self, title):
        self.title = title

    def win_enum_handler(self, hwnd, ctx):
        if self.title in win32gui.GetWindowText(hwnd):
            self.hwnd = hwnd

    def enumerate(self):
        win32gui.EnumWindows(self.win_enum_handler, None)
        try:
            self.hwnd
        except:
            print "No {} instance found, exiting".format(self.title)
            sys.exit(1)


class ScreenBits:
    def __init__(self, title):
        enumerator = EnumWind(title)
        enumerator.enumerate()
        self.hwnd = enumerator.hwnd
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        self.bitmap = win32ui.CreateBitmap()

    def _get_window_coordinates(self):
        l,t,r,b=win32gui.GetWindowRect(self.hwnd)
        #TODO: Margins should be customizable
        lm = 10#int(self.getProperty("leftmargin"))
        rm = 10#int(self.getProperty("rightmargin"))
        tm = 30#int(self.getProperty("topmargin"))
        bm = 10#int(self.getProperty("bottommargin"))
        h=b-t-(tm+bm)
        w=r-l-(rm+lm)
        return(l, t, r, b, h, w, lm, tm)

    def get_bitmap(self):
        print datetime.datetime.now()
        l, t, r, b, h, w, lm, tm = self._get_window_coordinates()
        self.bitmap.CreateCompatibleBitmap(self.mfcDC, w, h)
        saveDC=self.mfcDC.CreateCompatibleDC()
        saveDC.SelectObject(self.bitmap)
        saveDC.BitBlt((0,0),(w, h) , self.mfcDC, (lm,tm), win32con.SRCCOPY)
        self.bmpstr = self.bitmap.GetBitmapBits(True)
        self.bmpinfo = self.bitmap.GetInfo()
        self.im = Image.frombuffer('RGB', (self.bmpinfo['bmWidth'], self.bmpinfo['bmHeight']), self.bmpstr, 'raw', 'BGRX', 0, 1)


        print datetime.datetime.now()

        jpgname = os.path.abspath(os.path.join('.', 'selame'+".bmp"))
        print(os.path.abspath(jpgname))
        self.im.save(jpgname, format = 'jpeg', quality = 85)
        self.im.save(jpgname, format = 'bmp')
        saveDC.DeleteDC()
        #win32gui.DeleteObject(im.GetHandle())

class BitmapGrinder(ScreenBits):
    def __init__(self, title):
        ScreenBits.__init__(self, title)

    def find_windows_handles(self):
        print 'start searching handle', datetime.datetime.now()
        np_array = numpy.asarray(self.im)
        pattern = cv2.imread(os.path.abspath(os.path.join('.', 'pysx'+".bmp")))
        result = cv2.matchTemplate(np_array,pattern,cv2.TM_CCOEFF_NORMED)
        y,x = numpy.unravel_index(result.argmax(), result.shape)
        print ('x: ', x, 'y: ',y)
        print 'end searching handle', datetime.datetime.now()



#screen = BitmapGrinder('EVE')
screen = BitmapGrinder('Computer')
screen.get_bitmap()
screen.find_windows_handles()