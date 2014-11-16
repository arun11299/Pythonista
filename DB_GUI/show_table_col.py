# This module will create a new frame where the root user will enter
# the required columns needed for the new company's database
# This module is called by the module "show_database.py"
import wx.grid
import create_table

frame1 = None
glob_row_counter = None # Maintains number of rows present in the grid

class NewFrame(wx.Frame): # for Entering number of rows and columns
    def __init__(self,parent,id,name,operation):

        wx.Frame.__init__(self,parent,id,name,size = (300,300))
        panel = wx.Panel(self)
        if operation == "row":
            self.count_row = 0
            self.text = wx.StaticText(panel,-1,"No. of rows: ",size = (180,-1))
            self.dy_text = wx.TextCtrl(panel,-1,"",pos = (120,-1))
            self.button_add = wx.Button(panel,-1,"Enter",pos = (20,70))
            self.Bind(wx.EVT_BUTTON,self.OnAdd,self.button_add)
            self.button_dec = wx.Button(panel,-1,"I decline",pos = (120,70))
            self.Bind(wx.EVT_BUTTON,self.OnDecline,self.button_dec)
        else:
            pass

    def OnAdd(self,event):
        global glob_row_counter
        no_rows = self.dy_text.GetValue()
        if self.count_row == 0:
            d = wx.MessageDialog(self,"Are you sure,you want to add row?",\
                             "Warning!",wx.OK)
            self.count_row += 1
            d.ShowModal()
        else:
            if no_rows == "":
                f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                f.ShowModal()
            else:
                
                frame1.grid.AppendRows(numRows = int(no_rows))
                glob_row_counter += 1
                self.Close()

    def OnDecline(self,event):
        self.Destroy()



class CreateGrid(wx.grid.Grid): # Creates the grid for entering data
    def __init__(self,parent,cols,col_header):
        global glob_row_counter
        wx.grid.Grid.__init__(self, parent, -1)
        no_col = int(cols)
        no_row = 15          # Default number of rows

        glob_row_counter = no_row
        
        count = 0
        self.CreateGrid(no_row,no_col)
        print col_header
        for j in col_header:
            self.SetColLabelValue(count,j)
            count += 1
        print "Column headers done"

            
class CreateTabFrame(wx.Frame):  # Main Frame
    def __init__(self,parent,id,name,cols,comp_name_esc,conn,c,domain_name,\
                 col_header,col_header_esc,comp_name,major_name):
        
        self.domain_name = domain_name    
        self.cols = int(cols)
        self.comp_name_esc = comp_name_esc
        self.conn = conn
        self.c = c
        self.comp_name = comp_name
        self.major_name = major_name
        
        self.col_vals = [] # contains table names
        self.row_count = 0 # Excluding the row containing column names

        # Before creating the table grid ,we have to first get the
        # column header names.

        self.col_header = col_header
        self.col_header_esc = col_header_esc

        ###
        #print "follow"
        #print self.col_header
        wx.Frame.__init__(self,parent,id,name,size = (500,700))
        #self.panel = wx.Panel(self)
        self.grid = CreateGrid(self,self.cols,self.col_header)

        # MenuBar
        filemenu= wx.Menu()
        filemenu.Append(101, "&Add Row"," Adds a row")
        filemenu.Append(105,"&Add Column"," adds a column")
        filemenu.Append(110,"&Save Table"," saves the table")
        filemenu.AppendSeparator()
        filemenu.Append(115,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Options") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        wx.EVT_MENU(self, 110, self.OnClick1)
        wx.EVT_MENU(self, 101, self.OnClick2)
        wx.EVT_MENU(self, 105, self.OnClick3)
        wx.EVT_MENU(self, 115, self.OnExit)

    def OnClick1(self,event): # Enter Table
        # first read first row of the grid that gives the column headers

        global glob_row_counter
        
        ret_val = create_table.col_headers(self.conn,self.c,self.domain_name,\
                                 self.comp_name_esc,self.col_header_esc,\
                                           self.comp_name,self.major_name)
        if ret_val == 0:
            d = wx.MessageDialog(self,"Error while creating table",\
                             "Warning!",wx.OK)
            d.ShowModal()
        else:
            d = wx.MessageDialog(self,"Table created",\
                             "Message",wx.OK)
            d.ShowModal()

        # Now transfer the data present in cells to the database
            row_count = 0
            null_count = 0
            null_row = 0
            cell_data = []
            for row_count in range(glob_row_counter):
                for i in range(int(self.cols)):
                    cell_data.append(self.grid.GetCellValue(row_count,i))

                ret_val = create_table.enter_data(self.conn,self.c,\
                                                  self.domain_name,\
                                                  self.comp_name_esc,\
                                                  cell_data,self.comp_name)
                cell_data = []  # Reset the cell data list
                if ret_val == False:
                    d = wx.MessageDialog(self,"Error while entering data into table",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                
            d = wx.MessageDialog(self,"Data entered",\
                             "Message",wx.OK)
            d.ShowModal()
                    #self.Close()
        
        self.Close(True)
        
        

    def OnClick2(self,event): # Add Row
        frame1 = NewFrame(None,-5,"Inputs","row")
        frame1.Show(True)

    def OnClick3(self,event): # Add Column
        pass

    
    def OnExit(self,event):
        self.Close(True)

def main(cols,col_header,col_header_esc,\
                            comp_name_esc,conn,c,domain_name,comp_name,major_name):
    global frame1
    frame1 = CreateTabFrame(None,-1,"Create Columns",cols,\
                            comp_name_esc,conn,c,domain_name,col_header,\
                            col_header_esc,comp_name,major_name)
    frame1.Show(True)
        


    
