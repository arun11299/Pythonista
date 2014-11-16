''' This module implements the addition and removal of clients for the root
user window.This module is called by user_window.py'''
import wx
frame10 = None

class PopFrames(wx.Frame):
    def __init__(self,parent,id,name,operation,conn,c):
        if operation == "add":
            wx.Frame.__init__(self,parent,id,name,size = (360,240))
            self.conn = conn
            self.c = c

            self.panel = wx.Panel(self)
            self.st_text = wx.StaticText(self.panel,-1,"User Name: ",\
                                         size = (180,-1),pos = (5,7))
            self.dy_user = wx.TextCtrl(self.panel,-1,"",pos = (120,7))

            self.st_text2 = wx.StaticText(self.panel,-1,"Host: ",\
                                         size = (180,-1),pos = (5,45))
            self.dy_host = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

            self.st_text3 = wx.StaticText(self.panel,-1,"Password: ",\
                                         size = (180,-1),pos = (5,90))
            self.dy_passwd = wx.TextCtrl(self.panel,-1,"",pos = (120,90),style=wx.TE_PASSWORD)

            self.st_text4 = wx.StaticText(self.panel,-1,"Password: ",\
                                         size = (180,-1),pos = (5,135))
            self.dy_repasswd = wx.TextCtrl(self.panel,-1,"",pos = (120,135),style=wx.TE_PASSWORD)

            self.button = wx.Button(self.panel,-1,"Add",pos = (120,174))
            self.Bind(wx.EVT_BUTTON,self.AddUser,self.button)
            
        elif operation == "remove":
            wx.Frame.__init__(self,parent,id,name,size = (360,120))
            self.conn = conn
            self.c = c

            self.panel = wx.Panel(self)
            self.st_text = wx.StaticText(self.panel,-1,"User Name: ",\
                                         size = (180,-1),pos = (5,7))
            self.dy_user = wx.TextCtrl(self.panel,-1,"",pos = (120,7))

            self.st_text2 = wx.StaticText(self.panel,-1,"Host: ",\
                                         size = (180,-1),pos = (5,45))
            self.dy_host = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

            self.button = wx.Button(self.panel,-1,"Remove",pos = (120,75))
            self.Bind(wx.EVT_BUTTON,self.RmUser,self.button)
            

    def AddUser(self,event):
        user = "\""+self.dy_user.GetValue()+"\""
        host = "\""+self.dy_host.GetValue()+"\""
        passwd = "\""+self.dy_passwd.GetValue()+"\""
        re_passwd = "\""+self.dy_repasswd.GetValue()+"\""

        if self.dy_passwd.GetValue() == self.dy_repasswd.GetValue():
            self.c.execute('''use mysql''')
            self.c.execute('''select user,host from user''')

            user_info = self.c.fetchall()
            flag = True
        
            for i in range(len(user_info)):
                if user_info[i][0] == self.dy_user.GetValue():
                    if user_info[i][1] == self.dy_host.GetValue():
                        flag = False
                    else:
                        pass
                else:
                    pass
            if flag == True:
                self.c.execute('''create user %s@%s identified by %s'''\
                       %(user,host,passwd))
                self.conn.commit()
                d = wx.MessageDialog(self,"User Created",\
                             "Message",wx.OK)
                d.ShowModal()
                self.Close(True)
            else:
                d = wx.MessageDialog(self,"User already present with same hostname",\
                             "Warning!",wx.OK)
                d.ShowModal()
                self.Close(True)

        else:
            d = wx.MessageDialog(self,"Check your password",\
                             "Warning!",wx.OK)
            d.ShowModal()

    def RmUser(self,event):
        user = "\""+self.dy_user.GetValue()+"\""
        host = "\""+self.dy_host.GetValue()+"\""

        self.c.execute('''use mysql''')
        self.c.execute('''select user,host from user''')

        user_info = self.c.fetchall()
        flag = False
        
        for i in range(len(user_info)):
            if user_info[i][0] == self.dy_user.GetValue():
                if user_info[i][1] == self.dy_host.GetValue():
                    flag = True
                else:
                    pass
            else:
                pass
            
        if flag == False:
            d = wx.MessageDialog(self,"User/Host not present",\
                             "Warning!",wx.OK)
            d.ShowModal()
            self.Close(True)
        else:
            self.c.execute('''drop user %s@%s'''%(user,host))
            self.conn.commit()
            d = wx.MessageDialog(self,"User Deleted",\
                             "Message",wx.OK)
            d.ShowModal()
            self.Close(True)

class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,user_info):
        wx.grid.Grid.__init__(self,parent,-1)

        rows = len(user_info)

        self.CreateGrid(rows,2)
        self.SetColLabelValue(0,"User")
        self.SetColLabelValue(1,"Host")

        for i in range(rows):
            self.SetCellValue(i,0,user_info[i][0])
            self.SetCellValue(i,1,user_info[i][1])
        

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c):
        wx.Frame.__init__(self,parent,id,name,size = (300,400))
        self.conn = conn
        self.c = c

        self.c.execute('''use mysql''')
        self.c.execute('''select user,host from user''')

        self.user_info  = self.c.fetchall()
        self.grid = SimpleGrid(self,self.user_info)
        
        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        
        filemenu = wx.Menu()
        filemenu1 = wx.Menu()
        filemenu.Append(101, "&Add User", "Add a user")
        filemenu.AppendSeparator()
        filemenu.Append(105, "E&xit","Terminates the program")

        filemenu1.Append(110, "&Remove User","Remove a user")
        filemenu.AppendSeparator()
        filemenu1.Append(115, "E&xit","Terminates the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Add User")
        menuBar.Append(filemenu1,"&Remove User")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self,101,self.AddUser)
        wx.EVT_MENU(self,105,self.OnExit1)
        wx.EVT_MENU(self,110,self.RmUser)
        wx.EVT_MENU(self,115,self.OnExit2)

    def AddUser(self,event):
        frame11 = PopFrames(None,-1,"Add User","add",self.conn,self.c)
        frame11.Show(True)

    def OnExit1(self,event):
        self.Destroy()

    def RmUser(self,event):
        frame11 = PopFrames(None,-1,"Remove User","remove",self.conn,self.c)
        frame11.Show(True)

    def OnExit2(self,event):
        self.Destroy()
            
def add_remove(conn,c):
    global frame10
    frame10 = CreateFrame(None,-1,"Add User",conn,c)
    frame10.Show(True)


