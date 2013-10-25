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
        jpgname = os.path.join('.', 'selame'+".bmp")
        self.bmpstr = self.bitmap.GetBitmapBits(True)
        self.bmpinfo = self.bitmap.GetInfo()
        im = Image.frombuffer('RGB', (self.bmpinfo['bmWidth'], self.bmpinfo['bmHeight']), self.bmpstr, 'raw', 'BGRX', 0, 1).convert('L')
        print datetime.datetime.now()
        self.matrix = list(im.getdata())

        #filee = open('matix', 'w+')
        #filee.write(str(list(im.getdata())))
        #filee.close()
        print datetime.datetime.now()
        #im.save(jpgname, format = 'jpeg', quality = 85)
        im.save(jpgname, format = 'bmp')
        #saveDC.DeleteDC()
        #win32gui.DeleteObject(bitmap.GetHandle())

class BitmapGrinder(ScreenBits):
    handler_matrix=[[191, 191, 191, 191, 191, 191, 191, 191],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [191, 191, 191, 191, 191, 191, 191, 191],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [191, 191, 191, 191, 191, 191, 191, 191],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [191, 191, 191, 191, 191, 191, 191, 191]
                    ]
    def __init__(self, title):
        ScreenBits.__init__(self, title)


    def find_windows_handles(self):
        w=380
        h=59
        print self.bmpinfo['bmWidth']
        print self.bmpinfo['bmHeight']
        print w+h*self.bmpinfo['bmWidth']

        print self.matrix[w+h*self.bmpinfo['bmWidth']]
        for number, point in enumerate(self.matrix):
            no_match=0
            linelen=len(self.handler_matrix[0])
            new_line=[]
            for iterator in range(number, number+linelen):
                new_line.append(self.matrix[iterator])
            if new_line == self.handler_matrix[0] and not no_match:
                local_number = number
                for line_base in self.handler_matrix:
                    if new_line == line_base:
                        new_line = []
                        local_number = local_number+self.bmpinfo['bmWidth']
                        for iterator in range(local_number, local_number+linelen):
                            new_line.append(self.matrix[iterator])
                    else:
                        no_match=1
                        break












    #def grind_bitmap(self):


#screen = BitmapGrinder('EVE')
screen = BitmapGrinder('Computer')
screen.get_bitmap()
screen.find_windows_handles()