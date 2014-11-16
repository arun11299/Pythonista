# This module is called by module user_window.py.This module should display
# the present user's list and an option for changing their password's.

# This file can only be accessed by a root user.
import wx.grid
frame15 = None

class PopFrames(wx.Frame):
    def __init__(self,parent,id,name):
        wx.Frame.__init__(self,parent,id,name,size = (360,250))
        self.panel = wx.Panel(self)

        self.st_text = wx.StaticText(self.panel,-1,"User Name: ",\
                                         size = (180,-1),pos = (5,7))
        self.dy_user = wx.TextCtrl(self.panel,-1,"",pos = (160,7))

        self.st_text2 = wx.StaticText(self.panel,-1,"Host: ",\
                                         size = (180,-1),pos = (5,45))
        self.dy_host = wx.TextCtrl(self.panel,-1,"",pos = (160,45))

        self.st_text2 = wx.StaticText(self.panel,-1,"New Password: ",\
                                         size = (180,-1),pos = (5,90))
        self.nw_passwd = wx.TextCtrl(self.panel,-1,"",pos = (160,90),style=wx.TE_PASSWORD)

        self.st_text3 = wx.StaticText(self.panel,-1,"Re-enter Password: ",\
                                         size = (180,-1),pos = (5,130))
        self.re_passwd = wx.TextCtrl(self.panel,-1,"",pos = (160,130),style=wx.TE_PASSWORD)

        self.button = wx.Button(self.panel,-1,"Set",pos = (160,190))
        self.Bind(wx.EVT_BUTTON,self.OnSet,self.button)


    def OnSet(self,event):
        chk_flag = True
        user_name = self.dy_user.GetValue()
        host_name = self.dy_host.GetValue()
        nw_passwd = self.nw_passwd.GetValue()
        re_passwd = self.re_passwd.GetValue()
        

        for i in (nw_passwd,re_passwd,user_name,host_name):
            if i == '':
                chk_flag = False
                break
            else:
                pass
        
        if chk_flag == True:
            frame15.c.execute('''select user,host from user''')
            user_info = frame15.c.fetchall()
            for i in range(len(user_info)):
                if user_name == user_info[i][0] and host_name == user_info[i][1]:
                    chk_flag = False
                    break
                else:
                    pass
            if chk_flag == False:
                if nw_passwd == re_passwd:
                    user = "\""+user_name+"\""
                    host = "\""+host_name+"\""
                    set_passwd = "\""+nw_passwd+"\""
                    frame15.c.execute('''set password for %s@%s = password(%s)'''\
                                      %(user,host,set_passwd))
                    frame15.conn.commit()
                    self.Close(True)
                    pass
                else:
                    d = wx.MessageDialog(self,"Paswwords does'nt match.Please check.",\
                             "Warning!",wx.OK)
                    d.ShowModal()
            else:
                d = wx.MessageDialog(self,"User does not exists.",\
                             "Warning!",wx.OK)
                d.ShowModal()
        

        
class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,conn,c):
        wx.grid.Grid.__init__(self,parent)
        c.execute('''use mysql''')
        c.execute('''select user,host from user''')
        user_info = c.fetchall()
        numRows = len(user_info)
        numCols = 2

        self.CreateGrid(numRows,numCols)
        self.SetColLabelValue(0,"User")
        self.SetColLabelValue(1,"Host")
        
        for i in range(len(user_info)):
            self.SetCellValue(i,0,user_info[i][0])
            self.SetCellValue(i,1,user_info[i][1])

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c):
        wx.Frame.__init__(self,parent,id,name,size = (360,200))
        self.conn = conn
        self.c = c

        self.grid = SimpleGrid(self,self.conn,self.c)

        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        
        filemenu = wx.Menu()
        filemenu1 = wx.Menu()
        filemenu.Append(101, "&Set Password", "Sets the password for the selected user")
        filemenu.AppendSeparator()
        filemenu.Append(105, "E&xit","Terminates the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Set Password")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self,101,self.setPasswd)
        wx.EVT_MENU(self,105,self.OnExit)

    def setPasswd(self,event):
        frame9 = PopFrames(None,-2,"Change Password")
        frame9.Show(True)
        pass

    def OnExit(self,event):
        self.Destroy()
        pass

        
def main(conn,c):
    global frame15
    frame15 = CreateFrame(None,-1,"Set Password",conn,c)
    frame15.Show(True)
