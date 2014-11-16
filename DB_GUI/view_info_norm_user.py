# This module shows information regarding location and email/url
# of the company. These informations are presented in a grid format with
# the operations like addition of column,row,delete row/column and saving
# the table. This module is called by "show_company.py"

import wx.grid
import create_table
#import view_loc_create
import view_loc_norm_user
import view_table_norm_user

frame = None

present_cols_table = None
present_rows_table = None

class PopFrames(wx.Frame):
    def __init__(self,parent,id,name):
        wx.Frame.__init__(self,parent,id,name,size = (300,200))
        self.panel = wx.Panel(self)
        if name == "view location":
            self.st_text2 = wx.StaticText(self.panel,-1,"Enter Location: ",\
                                        pos = (1,-1),size=(180,-1))
            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (120,-1))

            self.button = wx.Button(self.panel,-1,"Enter",pos = (30,80))
            self.Bind(wx.EVT_BUTTON,self.OnLoc,self.button)

                                

    def OnLoc(self,event): # Method for viewing location
        country_name = self.dy_text2.GetValue()
        if country_name == "":
            d = wx.MessageDialog(self,"Do not leave the field blank",\
                             "Message",wx.OK)
            d.ShowModal()

        # check if country name exists or not
        else:
            index_flag = False
            for j in range(len(frame.col_headers)):
                if frame.col_headers[j] == "Country":
                    index_flag = True
                    break
                else:
                    pass
            if index_flag == True:
                country = []
                for i in range(present_rows_table):
                    country.append(frame.grid.GetCellValue(i,j))
            
                for i in country:
                    if country_name == i:
                        index_flag = True
                        break
                        pass
                    else:
                        index_flag = False
                        pass
                if index_flag == False:
                    d = wx.MessageDialog(self,"Country Not Found",\
                             "Message",wx.OK)
                    d.ShowModal()
                    
            ##
                else:
                    view_loc.show_locations(frame.conn,frame.c,frame.comp_name,\
                                    country_name)
            else:
                d = wx.MessageDialog(self,"Location Not Found",\
                                 "Warning!",wx.OK)
                d.ShowModal()
            self.Close(True)

class CreateGrid(wx.grid.Grid):
    def __init__(self,parent,col_header_data,cols,all_data):
        
        wx.grid.Grid.__init__(self,parent,-1)
        self.CreateGrid(present_rows_table,cols)
        count = 0
        
        if all_data == ():
            d = wx.MessageDialog(self,"Empty Table!!!",\
                             "Message!",wx.OK)
            d.ShowModal()
            for i in col_header_data:  #showing column headers in the grid
                self.SetColLabelValue(count,i)
                count += 1
            #self.Close(True)
        else:
            for i in col_header_data:  #showing column headers in the grid
                self.SetColLabelValue(count,i)
                count += 1
            for count_row in range(len(all_data)):
                #self.AppendRows(numRows = (count_row + 1))
                for count_col in range(cols):
                    self.SetCellValue(count_row,count_col,\
                                             all_data[count_row][count_col])
                    print self.GetCellValue(count_row,count_col)
            print "table has been displayed"
            print "no of rows",count_row

    def show_val(self,rows,cols):
        data = []
        for count_row in range(rows):
                #self.AppendRows(numRows = (count_row + 1))
                for count_col in range(cols):
                    data.append(frame.grid.GetCellValue(count_row,count_col))

        return(data)

    
class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,col_headers,all_data,info_tab,conn,c,\
                 present_cols_table,present_rows_table,domain_name,comp_name):
            
        wx.Frame.__init__(self,parent,id,name,size = (500,700))

        self.conn = conn
        self.c = c
        self.col_headers = col_headers
        self.all_data = all_data
        self.domain_name = domain_name
        self.comp_name = comp_name
        self.info_tab = info_tab
        #self.all_data = []
        
        self.cols = int(len(self.col_headers))
        #glob_col_count = self.cols
        #self.rows = glob_row_count
        #print "self.rows",self.rows
        #glob_row_count = 1
        self.grid = CreateGrid(self,self.col_headers,\
                               self.cols,self.all_data)

        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()

        # MenuBar for performing table related operations
        filemenu= wx.Menu()
        filemenu.AppendSeparator()
        filemenu.Append(125,"E&xit"," Terminate the program")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Operations") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        #filemenu1 = wx.Menu()
        #filemenu1.Append(130,"&Update Locations","Viewing locations")

        filemenu2 = wx.Menu()
        filemenu2.Append(135,"&View Locations","In the country")

        filemenu3 = wx.Menu()
        filemenu3.Append(140,"&Employee Database","View Employee Database")

        
        #menuBar.Append(filemenu1,"&Update Location")
        menuBar.Append(filemenu2,"&View Location")
        menuBar.Append(filemenu3,"&Employee Database")
        self.SetMenuBar(menuBar)

        wx.EVT_MENU(self, 125, self.OnExit)
        wx.EVT_MENU(self, 135, self.OnView)
        wx.EVT_MENU(self, 140, self.OnEmployee)
        

    # Defining menubar functions
    def OnView(self,event):
        view_frame = PopFrames(None,-6,"view location")
        view_frame.Show(True)
        pass

    def OnEmployee(self,event):
        view_table_norm_user.show_table(self.conn,self.c,self.domain_name,self.comp_name)

    def OnExit(self,event):
        self.Destroy()
        

def show_info(conn,c,domain_name,comp_name) :
    global frame
    global present_cols_table
    global present_rows_table

    info_tab = "`"+comp_name+"Info"+"`"

    c.execute('''show columns from %s'''%(info_tab))
    temp = c.fetchall()
    present_cols_table = len(temp)  # Very important
                               # maintains no of columns in the table
                               
    print present_cols_table
    col_headers = []
    for i in range(len(temp)):
        col_headers.append(temp[i][0])
        
    c.execute('''select * from %s'''%(info_tab))
    all_data = c.fetchall()

    present_rows_table = len(all_data)# Very important
                                      # maintains no of columns in the table 
    print present_rows_table
    
    frame = CreateFrame(None,-1,"General Info",col_headers,all_data,info_tab,\
                         conn,c,present_cols_table,present_rows_table,domain_name,\
                         comp_name)
    frame.Show(True)
