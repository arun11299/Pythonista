# This module will provide both root user and normal user with their respective
# windows.

import wx
import time
import import_file
import show_database
import show_database_norm_user
import client_operations
import set_passwd
import grant_priv

class UserWindow(wx.Frame):
    def __init__(self,parent,id,name,user_name,conn,c,host):
        # Required for Python-MySQL API
        self.conn = conn
        self.c = c

        if user_name == "root":
            wx.Frame.__init__(self,parent,id,name,size = (400,200))
            panel = wx.Panel(self)
            
            self.button1 = wx.Button(panel,-1,"Import from *.xls")
            self.Bind(wx.EVT_BUTTON,self.OnClick1,self.button1)

            self.button2 = wx.Button(panel,-1," Show Databases  ")
            self.Bind(wx.EVT_BUTTON,self.OnClick2,self.button2)

            self.button3 = wx.Button(panel,-1,"Add/Remove Client")
            self.Bind(wx.EVT_BUTTON,self.OnClick3,self.button3)

            #self.button4 = wx.Button(panel,-1,"  Remove Client  ")
            #self.Bind(wx.EVT_BUTTON,self.OnClick4,self.button4)

            self.button5 = wx.Button(panel,-1,"   Set Password  ")
            self.Bind(wx.EVT_BUTTON,self.OnClick5,self.button5)

            self.button6 = wx.Button(panel,-1," Grant Privileges")
            self.Bind(wx.EVT_BUTTON,self.OnClick6,self.button6)

            self.button7 = wx.Button(panel,-1,"      Backup     ")
            self.Bind(wx.EVT_BUTTON,self.OnClick7,self.button7)

            self.button8 = wx.Button(panel,-1,"  End Session    ")
            self.Bind(wx.EVT_BUTTON,self.OnClick8,self.button8)

            self.button9 = wx.Button(panel,-1,"      Close      ",\
                                     pos = (265,79))
            self.Bind(wx.EVT_BUTTON,self.OnClick9,self.button9)

            # Sizers
            sizer = wx.FlexGridSizer(cols=3, hgap=6, vgap=6)
            sizer.AddMany([self.button1,self.button2,self.button3,\
                           self.button5,self.button6,self.button7,self.button8\
                           ])
            panel.SetSizer(sizer)

        elif user_name != "root": #and host != "localhost":
            wx.Frame.__init__(self,parent,id,name,size = (380,220))
            panel = wx.Panel(self)

            self.button2_norm = wx.Button(panel,-1," Show Databases  ")
            self.Bind(wx.EVT_BUTTON,self.OnClick2_norm,self.button2_norm)

            self.button8 = wx.Button(panel,-1,"  End Session    ")
            self.Bind(wx.EVT_BUTTON,self.OnClick8,self.button8)

            self.button9 = wx.Button(panel,-1,"      Close      ",\
                                     pos = (265,79))
            self.Bind(wx.EVT_BUTTON,self.OnClick9,self.button9)

            sizer = wx.FlexGridSizer(cols=3, hgap=6, vgap=6)
            sizer.AddMany([self.button2_norm,self.button8,self.button9])
            panel.SetSizer(sizer)
            pass

            

    def OnClick1(self,event):   # Import Function
        import_file.main(self.conn,self.c)

    def OnClick2(self,event):   # Show database for super user
        show_database.main(self.conn,self.c)

    def OnClick2_norm(self,event):   # Show database for normal user
        show_database_norm_user.main(self.conn,self.c)

    def OnClick3(self,event):   # Add Client
        client_operations.add_remove(self.conn,self.c)

    #def OnClick4(self,event):   # Remove Client
        #client_operations.remove(self.conn,self.c)
        #pass

    def OnClick5(self,event):   # Set Password
        set_passwd.main(self.conn,self.c)
        pass

    def OnClick6(self,event):   # Grant Privileges
        grant_priv.main(self.conn,self.c)
        pass

    def OnClick7(self,event):   # Backup
        pass

    def OnClick8(self,event):   # Ending the session
        self.conn.close()
        pass

    def OnClick9(self,event):   # Final Flash
        self.Destroy()
def main(user_name,conn,c,host):
    frame = UserWindow(None,-1,"Database Management ",user_name,conn,c,host)
    frame.Show(True)
