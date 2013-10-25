import sys
import win32gui
import win32con
import timeit
import win32ui
import win32api
import os
import random
import Image

#MAYBE WE SHALL USE GetDIBits HERE!?
class ScreenShooter:
    def __init__(self):
       pass
    def get_info(self):
        self.hwin = win32gui.GetDesktopWindow()
        self.width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
        self.height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
        self.left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
        self.top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
        self.hwindc = win32gui.GetWindowDC(self.hwin)
        self.srcdc = win32ui.CreateDCFromHandle(self.hwindc)
        self.bmp = win32ui.CreateBitmap()
        self.bmp.CreateCompatibleBitmap(self.srcdc, self.width, self.height)
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.memdc.SelectObject(self.bmp)
    def generate_screen(self):
        self.memdc = self.srcdc.CreateCompatibleDC()
        self.bmp = win32ui.CreateBitmap()
        self.bmp.CreateCompatibleBitmap(self.srcdc, self.width, self.height)
        #buffer = self.bmp.GetBitmapBits()
        #print(len(buffer))
        self.memdc.SelectObject(self.bmp)
        self.memdc.BitBlt((0, 0), (self.width, self.height), self.srcdc, (self.left, self.top), win32con.SRCCOPY)
        self.bmp.SaveBitmapFile(self.memdc, 'screenshot{}.bmp'.format(random.randint(1, 40)))
    def make_bitmap(self):
        self.memdc.BitBlt((0, 0), (self.width, self.height), self.srcdc, (self.left, self.top), win32con.SRCCOPY)
        buffer = self.bmp.GetBitmapBits(True)
        print(len(buffer))
        return buffer
    def get_part(self, xp, xf, yp, yf):
        screen = self.make_bitmap()
        print screen[2:6]


class EnumWind:
    def __init__(self, title):
        self.title = title
    def win_enum_handler(self, hwnd, ctx):
        if self.title in win32gui.GetWindowText(hwnd):
            self.hwnd = hwnd
    def enumerate(self):
        win32gui.EnumWindows(self.win_enum_handler, None)



def another_try():
        #handle = 0
        objhandler = EnumWind('TeamSpeak')
        objhandler.enumerate()
        hwnd = objhandler.hwnd
        #print handle
        #hwnd = handle

        #hwnd = win32gui.EnumWindows( winEnumHandler, None )
        #hwnd = win32gui.GetWindow(hwndr, 4)
        #print hwnd
        #hwdc = win32gui.GetWindowDC(i_desktop_window_id)
        #hwnd = win32gui.GetDesktopWindow()
        print 'hwnd'

        print hwnd
        print 'end'
        l,t,r,b=win32gui.GetWindowRect(hwnd)
        lm = 10#int(self.getProperty("leftmargin"))
        rm = 10#int(self.getProperty("rightmargin"))
        tm = 30#int(self.getProperty("topmargin"))
        bm = 10#int(self.getProperty("bottommargin"))

        h=b-t-(tm+bm)
        w=r-l-(rm+lm)

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC=win32ui.CreateDCFromHandle(hwndDC)
        saveDC=mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0,0),(w, h) , mfcDC, (lm,tm), win32con.SRCCOPY)
        jpgname = os.path.join('.', 'selame'+".jpg")
        bmpstr = saveBitMap.GetBitmapBits(True)
        bmpinfo = saveBitMap.GetInfo()


            #bmpstr[num] = '1'

        im = Image.frombuffer('RGB', (bmpinfo['bmWidth'], bmpinfo['bmHeight']), bmpstr, 'raw', 'BGRX', 0, 1)

        #file_h = open('binary', 'w+')
        #file_h.write(im)
        #file_h.close()
        im.save(jpgname, format = 'jpeg', quality = 85)
        saveDC.DeleteDC()
        win32gui.DeleteObject(saveBitMap.GetHandle())


def screen_shooter():
    i_desktop_window_id = win32gui.EnumWindows( winEnumHandler, None )
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)
    hwin = win32gui.GetDesktopWindow()
    width = win32api.GetSystemMetrics(win32con.SM_CXVIRTUALSCREEN)
    height = win32api.GetSystemMetrics(win32con.SM_CYVIRTUALSCREEN)
    left = win32api.GetSystemMetrics(win32con.SM_XVIRTUALSCREEN)
    top = win32api.GetSystemMetrics(win32con.SM_YVIRTUALSCREEN)
    hwindc = win32gui.GetWindowDC(i_desktop_window_id)
    srcdc = win32ui.CreateDCFromHandle(hwindc)
    memdc = srcdc.CreateCompatibleDC()
    bmp = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(srcdc, width, height)
    memdc.SelectObject(bmp)
    memdc.BitBlt((0, 0), (width, height), srcdc, (left, top), win32con.SRCCOPY)
    buffer = bmp.GetBitmapBits() #<- CORE
    print(len(buffer))
    bmp.SaveBitmapFile(memdc, 'screenshot.bmp')


def winEnumHandler( hwnd, ctx ):
    #if win32gui.IsWindowVisible( hwnd ):
        if 'TeamSpeak' in win32gui.GetWindowText(hwnd):
            print 'returning hwnd'
            print hwnd

            print 'end'
            return hwnd
#    if 'TeamSpeak' in name:
#        print name

def get_pixel_colour(i_x, i_y, i_desktop_window_dc):
    #print(win32gui.GetWindowText('TeamSpeak 3'))

    long_colour = win32gui.GetPixel(i_desktop_window_dc, i_x, i_y)

    i_colour = int(long_colour)
    return (i_colour & 0xff), ((i_colour >> 8) & 0xff), ((i_colour >> 16) & 0xff)

def get_matrix(x_p, x_f, y_p, y_f):
    i_desktop_window_id = win32gui.EnumWindows( winEnumHandler, None )
    #win32gui.GetCur    rentPositionEx()
    i_desktop_window_dc = win32gui.GetWindowDC(i_desktop_window_id)

#    print(win32gui.GetCursorPos())
#    print(win32gui.DrawText(i_desktop_window_dc, 'String' , -1 , (300,300,400,400), win32con.DT_LEFT ))
    print 'handled'
    matrixy = []

    for y in range(y_p, y_f):
        matrixx= []

        for x in range(x_p, x_f):
            #win32gui.
            matrixx.append(get_pixel_colour(x, y, i_desktop_window_dc))
            #win32gui.SetPixel(win32gui.GetDC(i_desktop_window_id),x,y,128)
        matrixy.append(matrixx)


    return matrixy


#print(get_matrix(1,1,10,10))
def printer():
    for line in get_matrix(100,110,100,110):
        print(line)
#print get_pixel_colour(6, 6)

screen = ScreenShooter()
screen.get_info()
screen.generate_screen()
screen.get_part('1','10','1','10')
#screen_shooter()
another_try()


#print(timeit.timeit(stmt=s, setup="from __main__ import ScreenShooter", number=1))
#screen_shooter()
#print(timeit.timeit("printer()", setup="from __main__ import printer", number=1))