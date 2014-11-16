# This is the main GUI that will give an option of getting access to
# the daily delivery database and the company database
import wx
import about_box
import authentication
import time
class MainFrame(wx.Frame):
    def __init__(self,parent,id,name):
         # SplashScreen
        image = wx.Image("/home/arun/Code_project/vegito.bmp", wx.BITMAP_TYPE_BMP)
        bmp = image.ConvertToBitmap()
        wx.SplashScreen(bmp, wx.SPLASH_CENTRE_ON_SCREEN |
        wx.SPLASH_TIMEOUT, 3000, None, -1)
        wx.Yield()
        time.sleep(0.7)
        wx.Frame.__init__(self,parent,id,name,size = (300,200))
        panel = wx.Panel(self)
        panel.SetBackgroundColour('grey')

        filemenu = wx.Menu()
        filemenu.Append(101, "&About","Software Info")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&About")
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, 101, self.About)
       
        #
        wx.StaticText(panel,-1,"Where Do You Want To Go?",pos = (55,60))
        self.button1 = wx.Button(panel,-1,"Daily Delivery",pos = (40,100))
        self.Bind(wx.EVT_BUTTON,self.OnClickDelv,self.button1)

        self.button2 = wx.Button(panel,-1,"   Database   ",pos = (150,100))
        self.Bind(wx.EVT_BUTTON,self.OnClickDbase,self.button2)

        self.button3 = wx.Button(panel,-1,"  Exit  ",pos = (105,145))
        self.Bind(wx.EVT_BUTTON,self.OnExit,self.button3)

    def OnClickDelv(self,event):
        pass
        #self.Close()

    def OnClickDbase(self,event):
        authentication.main()
        #self.Close()

    def About(self,event):
        about_box.main()

    def OnExit(self,event):
        self.Destroy()
        
app = wx.PySimpleApp()
frame = MainFrame(None,-1,"Getting Started")
frame.Show(True)
app.MainLoop()
