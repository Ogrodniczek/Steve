import sys
import win32gui
import win32con
import win32ui
import os
import Image
import datetime


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
        self.enumerator = EnumWind(title)

    def initialize_window(self):
        self.enumerator.enumerate()
        self.hwnd = self.enumerator.hwnd
        hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(hwndDC)


    def _get_window_coordinates(self):
        #Windows 7 margins
        lm = 10
        rm = 10
        tm = 30
        bm = 10
        l,t,r,b=win32gui.GetWindowRect(self.hwnd)
        h=b-t-(tm+bm)
        w=r-l-(rm+lm)
        return(l, t, r, b, h, w, lm, tm)


    def refresh_image(self):
        then = datetime.datetime.now()
        l, t, r, b, h, w, lm, tm = self._get_window_coordinates()
        self.bitmap = win32ui.CreateBitmap()
        self.bitmap.CreateCompatibleBitmap(self.mfcDC, w, h)


        saveDC = self.mfcDC.CreateCompatibleDC()
        saveDC.SelectObject(self.bitmap)
        saveDC.BitBlt((0,0),(w, h) , self.mfcDC, (lm,tm), win32con.SRCCOPY)
        self.bmpstr = self.bitmap.GetBitmapBits(True)
        self.bmpinfo = self.bitmap.GetInfo()
        self.im = Image.frombuffer('RGB', (self.bmpinfo['bmWidth'],
                                           self.bmpinfo['bmHeight']),
                                   self.bmpstr, 'raw', 'BGRX', 0, 1)
        saveDC.DeleteDC()
        print 'refresh image ', datetime.datetime.now()-then

    def save_window_image(self):
        bmpname = os.path.abspath(os.path.join('.', 'grabbed'+".bmp"))
        print(os.path.abspath(bmpname))
        self.im.save(bmpname, format = 'bmp')