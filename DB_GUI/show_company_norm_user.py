# This module is called by "show_database.py".This module basically
# displays all the companys that comes under the major company name.


import wx.grid
import view_info_norm_user

frame9 = None

class PopFrames(wx.Frame):
    def __init__(self,parent,id,name,conn,c,xtra_info = None):
        self.xtra_info = xtra_info
        if name == "Notice":
            self.count = 0
            wx.Frame.__init__(self,parent,id,name,size = (300,120))
            self.panel = wx.Panel(self)
            self.conn = conn
            self.c = c

            self.st_text = wx.StaticText(self.panel,-1,"Notice: ",\
                                    size = (180,-1),pos = (5,45))
            self.dy_text = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

            self.button = wx.Button(self.panel,-1,"Flag It",pos = (120,80))
            self.Bind(wx.EVT_BUTTON,self.OnFlagIt,self.button)

        
    def OnFlagIt(self,event):
        global frame9
        comp_name = self.xtra_info
        comp_name_new = "\""+comp_name+"\""
        notice = self.dy_text.GetValue()
        notice_new = "\""+notice+"\""

        self.c.execute('''update LastView set Flag = %s where `Company Name` = %s'''\
                       %(notice_new,comp_name_new))
        self.conn.commit()
        self.Close(True)

        
    
class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,actual_company):
        wx.grid.Grid.__init__(self,parent)

        row = len(actual_company)
        col = 1
        self.CreateGrid(row,col)
        self.SetColLabelValue(0,"Subfolders")

        for i in range(row):
            for j in range(col):
                self.SetCellValue(i,j,actual_company[i])
                

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c,domain_name,\
                 actual_company):
        wx.Frame.__init__(self,parent,id,name,size = (300,400))

        self.actual_company = actual_company
        self.grid = SimpleGrid(self,self.actual_company)
        
        self.conn = conn
        self.c = c
        self.domain_name = domain_name
        
        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        
        filemenu = wx.Menu()
        filemenu.Append(101, "&Info & Employee Details","View Company Information")
        
        filemenu.AppendSeparator()
        filemenu.Append(125,"E&xit"," Terminate the program")

        
        filemenu1 = wx.Menu()
        filemenu1.Append(135,"&Flag Company","Any Notification about company")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Details") # Adding the "filemenu" to the MenuBar
        menuBar.Append(filemenu1,"&Flag Info")
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.
        
        wx.EVT_MENU(self, 101, self.ViewInfo)
        
        wx.EVT_MENU(self, 125, self.OnExit)
        
        wx.EVT_MENU(self, 135, self.OnFlag)

    def ViewInfo(self,event):
        #compiz = PopFrames(None,-7,"Give Details",self.conn,self.c)
        #compiz.Show(True)
        self.sel_comp = None
        for i in range(len(self.actual_company)):
            if self.grid.IsInSelection(i,0):
                self.sel_comp = self.grid.GetCellValue(i,0)
                break
            else:
                pass
        if self.sel_comp == None:
            d = wx.MessageDialog(self,"Select at least one company",\
                             "Warning!",wx.OK)
            d.ShowModal()
        else:
            view_info_norm_user.show_info(frame9.conn,frame9.c,frame9.domain_name,\
                                self.sel_comp)
        self.Close(True)


    def OnFlag(self,event):
        self.sel_comp = None
        for i in range(len(self.actual_company)):
            if self.grid.IsInSelection(i,0):
                self.sel_comp = self.grid.GetCellValue(i,0)
                break
            else:
                pass
        if self.sel_comp == None:
            d = wx.MessageDialog(self,"Select at least one company",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:
            Flag = PopFrames(None,-7,"Notice",self.conn,self.c,self.sel_comp)
            Flag.Show(True)
            pass
        #self.Close(True)
        
    def OnExit(self,event):
        self.Close(True)

def main(conn,c,domain_name,actual_company):
    global frame9

    frame9 = CreateFrame(None,-7,"Company(s)",conn,c,domain_name,\
                         actual_company)
    frame9.Show(True)
