# This Module Will Build The Password Module Required For Authentication

import wx
import time
import login_db
import user_window

class Authentication(wx.Frame):
    def __init__(self,parent,id,name):
        wx.Frame.__init__(self,parent,id,name,size = (400,250))
        panel = wx.Panel(self)
        # Username
        self.st_text = wx.StaticText(panel,-1,"Username: ",pos = (5,7))
        self.dy_text = wx.TextCtrl(panel,-1,"",size = (175,-1),pos = (100,7))
        #self.dy_text.SetInsertionPoint(0)

        # Password
        self.st_passwd = wx.StaticText(panel,-1,"Password: ",pos = (5,47))
        self.dy_passwd = wx.TextCtrl(panel,-1,"",size = (175,-1),\
                                     pos = (100,47),style=wx.TE_PASSWORD)
        #self.dy_passwd.SetInsertionPoint(0)

        # Host Name
        self.st_host = wx.StaticText(panel,-1,"Host: ",pos = (5,87))
        self.dy_host = wx.TextCtrl(panel,-1,"",size = (175,-1),pos = (100,87))
        #self.dy_host.SetInsertionPoint(0)

        
        # Login Button
        self.button = wx.Button(panel,-1,"Login",pos = (140,142))
        self.Bind(wx.EVT_BUTTON,self.LogIn,self.button)

        

    def LogIn(self,event):
        count = 0
        flag = True
        user_name = self.dy_text.GetValue()
        password = self.dy_passwd.GetValue()
        host_name = self.dy_host.GetValue()


        #database = self.dy_database()
        #self.status.Clear()
        for entry in (user_name,password,host_name):
            if entry == "":
                flag = False
                break
            else:
                pass
            
        if flag == True:
            [ret_val,conn,c] = login_db.login(user_name,password,host_name)
            if ret_val == 1:
                #self.status.SetValue("Authenticated")
                time.sleep(0.7)
                user_window.main(user_name,conn,c,host_name) # passing conn,c to next level
                self.Close()
            else:
                #self.status.Clear()
                #self.status.SetValue("Unable To Authenticate")
                d = wx.MessageDialog(self,"Check Your Username/Password/host","Warning!",wx.OK)
                d.ShowModal()
                self.Destroy()

        else:
            d = wx.MessageDialog(self,"Fill All The Entries.:-X","Warning!",wx.OK)
            d.ShowModal()
            
        
        
def main():
    #app = wx.PySimpleApp()
    frame = Authentication(None,-1,"Authentication")
    frame.Show(True)
    #app.MainLoop()
