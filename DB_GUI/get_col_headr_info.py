# This module passes the column header names to the module "show_table_col.py"
import wx.grid
import show_table_col
frame2 = None

class CreateGrid(wx.grid.Grid):
    def __init__(self,parent,cols):
        wx.grid.Grid.__init__(self, parent, -1)
        no_col = int(cols)
        no_row = 1          # Default number of rows
        self.CreateGrid(no_row,no_col)

class GetColHeader(wx.Frame):
    def __init__(self,parent,id,name,cols,comp_name_esc,\
                          conn,c,domain_name,comp_name,major_name):
        self.col_header = ["Employee ID"]
        self.col_header_esc = ["`Employee ID`"]
        self.cols = int(cols)
        self.comp_name_esc = comp_name_esc # already escaped with `` in show_database.py
        self.conn = conn
        self.c = c
        self.domain_name = domain_name
        self.comp_name = comp_name
        self.major_name = major_name
        
        wx.Frame.__init__(self,parent,id,name,size = (500,300))
        #self.panel = wx.Panel(self)
        self.grid = CreateGrid(self,self.cols)

        # Menubar
        filemenu= wx.Menu()
        filemenu.Append(101, "&Done"," selects file")
        filemenu.AppendSeparator()
        filemenu.Append(105,"E&xit"," Terminate the program")

        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Save") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        wx.EVT_MENU(self, 101, self.OnClick)
        wx.EVT_MENU(self, 105, self.OnExit)

       
    def OnClick(self,event): # Gets the cell value which correspond to
                             # column headers for the gid in "show_table_col.py"           
        global frame2
        #self.col_header = []
        #self.col_header_esc = []
        flag = True
        #print self.cols
        for i in range(int(self.cols)):
            val = self.grid.GetCellValue(0,i)
            #print "index: ",i
            #val = self.grid.GetCellValue(0,2)
            #print val
            if val == "":
                flag = False
                #print "here"
                f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                f.ShowModal()
                break
            else:
                self.col_header.append(val)
                val = "`"+val+"`"
                self.col_header_esc.append(val)
        self.col_header.append("Remarks")
        self.col_header_esc.append("`Remarks`")
        self.cols = self.cols + 2
        #print "col header",frame2.col_header
        if flag == True:
            show_table_col.main(self.cols,self.col_header,self.col_header_esc,\
                            self.comp_name_esc,self.conn,self.c,\
                                self.domain_name,self.comp_name,self.major_name)
        

    def OnExit(self,event):
        self.Close(True)

        
def main(cols,comp_name_esc,conn,c,domain_name,comp_name,major_name):
    global frame2
    global flag
    frame2 = GetColHeader(None,-1,"Getting header info",cols,comp_name_esc,\
                          conn,c,domain_name,comp_name,major_name)
    frame2.Show()
    #return(frame2.col_header,frame2.col_header_esc,flag)
    #print "col: ",frame2.col_header
    #return(0,0)
