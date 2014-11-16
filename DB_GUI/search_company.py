# This module is for searching companies.This module is called by
# "show_database.py".

import wx.grid
import view_info

frame12 = None

class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,search_data):
        wx.grid.Grid.__init__(self,parent,-1)
        self.CreateGrid(0,1)
        self.SetColLabelValue(0,"Company Name")

        for i in range(len(search_data)):
            self.AppendRows(numRows = 1)
            self.SetCellValue(i,0,search_data[i])
        
class Frames(wx.Frame):
    def __init__(self,parent,id,name,conn,c,domain_name):
        wx.Frame.__init__(self,parent,id,name,size = (300,150))
        panel = wx.Panel(self)
        self.conn = conn
        self.c = c
        self.domain_name = domain_name
        
        self.st_text = wx.StaticText(panel,-1,"Company Name: ",\
                                         size = (180,-1),pos = (5,10))

        self.dy_text = wx.TextCtrl(panel,-1,"",pos = (130,10))

        self.button = wx.Button(panel,-1,"View",pos = (130,75))
        self.Bind(wx.EVT_BUTTON,self.OnInfo,self.button)

    def OnInfo(self,event):
        global frame12
        comp_name = self.dy_text.GetValue()
        view_info.show_info(self.conn,self.c,self.domain_name,comp_name)
        self.Close(True)
        
class PopFrames(wx.Frame):
    def __init__(self,parent,id,name,conn,c,srch_comp,\
                 domain_name):#srch_compis domain name for view info
        self.conn = conn
        self.c = c
        self.domain_name = domain_name
        if name == "Search Results":
            #print "searching for: ",srch_comp
            wx.Frame.__init__(self,parent,id,name,size = (400,600))

            filemenu = wx.Menu()
            filemenu.Append(101, "&View Company Info","View Company Information")
            filemenu.AppendSeparator()
            filemenu.Append(105,"E&xit","Terminate The Program")
            menuBar = wx.MenuBar()
            menuBar.Append(filemenu,"&View")
            self.SetMenuBar(menuBar)

            wx.EVT_MENU(self, 101, self.ViewInfo)
            wx.EVT_MENU(self, 105, self.OnExit)
            
            c.execute('''show tables''')
            data = c.fetchall()
            data_new = []
            for i in range(len(data)):
                table = data[i][0]
                tl1 = len(table) - 4
                tl2 = len(table) - 8
                if table[tl1:] != "Info" and table[tl2:] != "Location":
                    data_new.append(table)
                else:
                    pass
            #print "table list is:",data_new
            
            list_srch_comp = list(srch_comp)
            self.search_data = []
        
            chk_flag = False
            if list_srch_comp.pop() == "*":
                srch_comp_new = srch_comp[:(len(srch_comp) - 1)]
                length = len(srch_comp_new)

                for comp in data_new:
                    if comp[:length] == srch_comp_new:
                        self.search_data.append(comp)
                        chk_flag = True
                    else:
                        pass
                
                if chk_flag == False:
                    f = wx.MessageDialog(self,"Company %s does not exist "%(srch_comp_new),\
                             "Warning!",wx.OK)
                    f.ShowModal()
                    self.Close(True)

                else:
                    self.grid = SimpleGrid(self,self.search_data)
            else:
                for comp in data_new:
                    if comp == srch_comp:
                        chk_flag = True
                        self.search_data.append(comp)
                    else:
                        pass
                if chk_flag == False:
                    f = wx.MessageDialog(self,"Company %s does not exist "%(srch_comp),\
                             "Warning!",wx.OK)
                    f.ShowModal()
                    self.Close(True)

                else:
                    self.grid = SimpleGrid(self,self.search_data)

        
    def ViewInfo(self,event):
        global frame12
        self.sel_comp = None
        for i in range(len(self.search_data)):
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
            view_info.show_info(self.conn,self.c,self.domain_name,\
                                self.sel_comp)
        self.Close(True)
        #frame1 = Frames(None,-1,"View Info",self.conn,self.c,self.domain_name)
        #frame1.Show(True)

    def OnExit(self,event):
        self.Destroy()

              
class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c,domain_name):

        self.conn = conn
        self.c = c
        self.domain_name = domain_name
        
        wx.Frame.__init__(self,parent,id,name,size = (300,90))
        self.panel = wx.Panel(self)

        self.st_text = wx.StaticText(self.panel,-1,"Company Name: ",\
                                     size = (180,-1),pos = (5,7))
        self.dy_text = wx.TextCtrl(self.panel,-1,"",pos = (125,7))

        self.button = wx.Button(self.panel,-1,"Search",pos = (125,57))
        self.Bind(wx.EVT_BUTTON,self.OnSearch,self.button)

        
        
   
    
    def OnSearch(self,event):
        srch_comp = self.dy_text.GetValue()
        frame = PopFrames(None,-1,"Search Results",self.conn,self.c,srch_comp,\
                          self.domain_name)
        frame.Show(True)
        self.Close(True)

    

                
def main(conn,c,domain_name):
    global frame12
    frame12 = CreateFrame(None,-1,"Search Company",conn,c,domain_name)
    frame12.Show(True)
