import wx
from Grabber import BitmapGrinder
import os
#app = wx.App()
#frame = wx.Frame(None, -1, "Steve")

#image = wx.wxImage('icon.png', wxBITMAP_TYPE_PNG).ConvertToBitmap()
#icon = wx.wxEmptyIcon()
#icon.CopyFromBitmap(image)
#frame.SetIcon(icon)
#frame.SetSize(wx.Size(200,400))

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)
        panel = wx.Panel(self, -1)
        wx.Button(panel, 1, "Init", (0,0))
        wx.Button(panel, 10, "Start", (0,25))
        wx.Button(panel, 20, "Stop", (0,50))
        wx.Button(panel, 30, "Click", (0,75))
        #wx.Button(panel, -1, "", (0,50))
        self.Bind(wx.EVT_BUTTON, self.Init, id=1)
        self.Bind(wx.EVT_BUTTON, self.Start, id=10)
        self.Bind(wx.EVT_BUTTON, self.Stop, id=20)
        self.Bind(wx.EVT_BUTTON, self.Click, id=30)

    def Init(self, event):
        print('Init')
        self.screen = BitmapGrinder('EVE - ')
        self.screen.initialize_window()
        self.screen.refresh_image()
    def Start(self, event):
        print('Start')
        self.screen.find_pattern(os.path.abspath(os.path.join('.', 'Overview'+".bmp")))
    def Stop(self, event):
        self.screen.save_window_image()
        print('Stop')

    def Click(self, event):
        click(600, 300)
        click(600, 700)
        print('click')

def click(x,y):
    import win32api, win32con
    win32api.SetCursorPos((x,y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Steve')
        frame.Show(True)
        frame.SetSize(wx.Size(200,400))
        return True

app = MyApp(0)
app.MainLoop()