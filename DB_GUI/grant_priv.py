# This module is used for giving privileges to the normal user by root user.
# This module is called by the module "user_window.py".

import wx.grid
import get_grid_info

frame16 = None

class PopFrames(wx.Frame):
    def __init__(self,parent,id,name,sel_domain):
        wx.Frame.__init__(self,parent,id,name,size = (300,210))
        self.panel = wx.Panel(self)

        self.sel_domain = sel_domain

        self.st_user = wx.StaticText(self.panel,-1,"User: ",size = (180,-1),\
                                     pos = (5,45))
        self.dy_user = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

        self.st_host = wx.StaticText(self.panel,-1,"Host: ",size = (180,-1),\
                                     pos = (5,95))
        self.dy_host = wx.TextCtrl(self.panel,-1,"",pos = (120,95))

        self.st_passwd = wx.StaticText(self.panel,-1,"Password: ",size = (180,-1),\
                                     pos = (5,145))
        self.dy_passwd = wx.TextCtrl(self.panel,-1,"",pos = (120,145),style= wx.TE_PASSWORD)

        self.button = wx.Button(self.panel,-1,"Grant",pos = (120,180))
        self.Bind(wx.EVT_BUTTON,self.OnGrantIt,self.button)


    def OnGrantIt(self,event):
        user = self.dy_user.GetValue()
        host = self.dy_host.GetValue()
        passwd = self.dy_passwd.GetValue()

        chk_flag = True
        # Check for blank entry
        for i in (user,host,passwd):
            if i == "":
                chk_flag = False
                break
            else:
                pass

        if chk_flag == False:
            d = wx.MessageDialog(self,"Fill in all entries!!",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:  # All data filled

            # check if the user exists
            frame16.c.execute('''use mysql''')
            frame16.c.execute('''select user,host from user''')
            data = frame16.c.fetchall()

            for i in range(len(data)):
                if user == data[i][0] and host == data[i][1]:
                    chk_flag = True
                    break
                else:
                    chk_flag = False
                    pass

            if chk_flag == False:
                d = wx.MessageDialog(self,"User does not exist!",\
                             "Warning!",wx.OK)
                d.ShowModal()

            else:
                # Check if password is correct
                user_new = "\""+user+"\""
                host_new = "\""+host+"\""
                passwd_new = "\""+passwd+"\""
                try:
                    frame16.c.execute('''grant select on %s.* to %s@%s identified by %s'''\
                                  %(self.sel_domain,user_new,host_new,passwd_new))
                    frame16.conn.commit()
                    frame16.c.execute('''grant insert on %s.* to %s@%s identified by %s'''\
                                  %(self.sel_domain,user_new,host_new,passwd_new))
                    frame16.conn.commit()
                    #frame16.c.execute('''grant show databases on %s.* to %s@%s identified by %s'''\
                    #              %(self.sel_domain,user_new,host_new,passwd_new))
                    #frame16.c.execute('''grant alter on %s.* to %s@%s identified by %s'''\
                    #              %(self.sel_domain,user_new,host_new,passwd_new))
                    #frame16.c.execute('''grant create on %s.* to %s@%s identified by %s'''\
                    #              %(self.sel_domain,user_new,host_new,passwd_new))
                    #frame16.c.execute('''grant delete on %s.* to %s@%s identified by %s'''\
                    #              %(self.sel_domain,user_new,host_new,passwd_new))
                    #frame16.c.execute('''grant drop on %s.* to %s@%s identified by %s'''\
                    #              %(self.sel_domain,user_new,host_new,passwd_new))
                    frame16.c.execute('''grant update on %s.* to %s@%s identified by %s'''\
                                  %(self.sel_domain,user_new,host_new,passwd_new))
                    frame16.conn.commit()

                except:
                    d = wx.MessageDialog(self,"Incorrect Password!",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                self.Close(True)
                    
            


        
class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,domain,numRows):
        wx.grid.Grid.__init__(self,parent)
        self.CreateGrid(len(numRows),1)
        self.SetColLabelValue(0,"Domains")

        for i in range(len(domain)):
            self.SetCellValue(i,0,domain[i])

        
class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c):
        wx.Frame.__init__(self,parent,id,name,size = (340,220))

        [domain,numRows] = get_grid_info.main(conn,c,"show_database")
        self.domain = domain
        self.conn  = conn
        self.c = c
        
        self.grid = SimpleGrid(self,domain,numRows)

        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()

        filemenu = wx.Menu()
        filemenu.Append(101,"&Grant","Grants privileges to the specified user")
        filemenu.AppendSeparator()
        filemenu.Append(105,"E&xit","Terminates the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Grant Privileges")
        self.SetMenuBar(menuBar)
        
        wx.EVT_MENU(self,101,self.OnGrant)
        wx.EVT_MENU(self,105,self.OnExit)


    def OnGrant(self,event):
        self.sel_domain = None
        for i in range(len(self.domain)):
            if self.grid.IsInSelection(i,0):
                self.sel_domain = self.grid.GetCellValue(i,0)
                break
            else:
                pass

        if self.sel_domain == None:
            d = wx.MessageDialog(self,"Select at least one domain.",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:
            frame17 = PopFrames(None,-2,"Grant Privileges",self.sel_domain)
            frame17.Show(True)
                
        pass

    def OnExit(self,event):
        self.Destroy()
        
      
def main(conn,c):
    global frame16
    frame16 = CreateFrame(None,-1,"Grant Privileges",conn,c)
    frame16.Show(True)
