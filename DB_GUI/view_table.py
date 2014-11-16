# This module shows/displays the contents of the selected table.This module
# is called by the module "view_info.py"

import wx.grid
import create_table
import time
import Google

frame6 = None
present_cols_table = None
present_rows_table = None

# Class for making pop up kind of frames
class PopFrames(wx.Frame):
    def __init__(self,parent,id,name):
        wx.Frame.__init__(self,parent,id,name,size = (300,200))
        self.panel = wx.Panel(self)
        if name == "Add Rows":
            self.st_text = wx.StaticText(self.panel,-1,"No. of rows: ",size=(180,-1))
            self.dy_text = wx.TextCtrl(self.panel,-1,"",pos= (120,-1))

            self.button = wx.Button(self.panel,-1,"Enter",pos = (30,80))
            self.Bind(wx.EVT_BUTTON,self.OnAddRow,self.button)

        elif name == "Add Cols":
            
            self.st_text2 = wx.StaticText(self.panel,-1,"Position: ",\
                                          pos = (1,30),size=(180,-1))
            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (120,30))

            self.st_text3 = wx.StaticText(self.panel,-1,"Column Name: ",\
                                          pos = (1,60),size=(180,-1))
            self.dy_text3 = wx.TextCtrl(self.panel,-1,"",pos = (120,60))

            self.button = wx.Button(self.panel,-1,"Enter",pos = (30,80))
            self.Bind(wx.EVT_BUTTON,self.OnAddCol,self.button)

        elif name == "Delete Rows":
            self.st_text = wx.StaticText(self.panel,-1,"No. of rows: ",size=(180,-1))
            self.dy_text = wx.TextCtrl(self.panel,-1,"",pos= (120,-1))

            self.st_text2 = wx.StaticText(self.panel,-1,"Position: ",\
                                          pos = (1,30),size=(180,-1))
            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (120,30))

            self.button = wx.Button(self.panel,-1,"Enter",pos = (30,80))
            self.Bind(wx.EVT_BUTTON,self.OnDelRow,self.button)

        elif name == "Delete Column":
            self.st_text2 = wx.StaticText(self.panel,-1,"Position: ",\
                                        pos = (1,30),size=(180,-1))
            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (120,30))

            self.button = wx.Button(self.panel,-1,"Enter",pos = (30,80))
            self.Bind(wx.EVT_BUTTON,self.OnDelCol,self.button)

        elif name == "Searching":
            self.st_text = wx.StaticText(self.panel,-1,"Select Column: ",\
                                         pos = (10,10),size = (180,-1))

            self.button = wx.Button(self.panel,-1,"Select",pos = (150,10))
            self.Bind(wx.EVT_BUTTON,self.OnSel,self.button)

            self.st_text2 = wx.StaticText(self.panel,-1,"Search Box: ",\
                                          pos = (10,65),size = (180,-1))

            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (150,65))
            
            self.button1 = wx.Button(self.panel,-1,"Google",pos = (100,110))
            self.Bind(wx.EVT_BUTTON,self.OnGoogle,self.button1)

            
    def OnAddRow(self,event):

        global present_cols_table
        global present_rows_table
        
        no_rows = int(self.dy_text.GetValue())
        
        present_rows_table = present_rows_table + no_rows

        frame6.grid.AppendRows(numRows = no_rows)
        self.Close(True)
        pass

    def OnAddCol(self,event):
        # Only one column is allowed to be added at a time for
        # simplicity reasons.
        # "buffer_col_val" is being used because after adding a column
        # from the grid the column headers of all other columns gets changed

        global present_cols_table
        global present_rows_table
        
        pos = int(self.dy_text2.GetValue())
        col_name = self.dy_text3.GetValue()

        buffer_col_val = frame6.grid.GetColLabelValue((pos - 1))
        
        
        present_cols_table = present_cols_table + 1
        
        # if Position field is left blank new column(s) will get
        # appended to the last row in the grid.
        
        if self.dy_text2.GetValue() != "":
            frame6.grid.InsertCols(pos = (pos - 1),numCols = 1)
            frame6.grid.SetColLabelValue(pos,buffer_col_val)
        else:
            frame6.grid.AppendCols(numCols = 1)
            
        frame6.grid.SetColLabelValue((pos-1),col_name)
        self.Close(True)

    def OnDelRow(self,event):
        global present_cols_table
        global present_rows_table
        
        pos = int(self.dy_text2.GetValue()) - 1

        present_rows_table = present_rows_table - 1
        
        no_rows = int(self.dy_text.GetValue())
        frame6.grid.DeleteRows(pos = pos , numRows = no_rows)
        self.Close(True)


    def OnDelCol(self,event):
        
        # Only one column is allowed to be deleted at a time for
        # simplicity reasons.
        # "buffer_col_val" is being used because after deleting a column
        # from the grid the column headers of all other columns gets changed
        global present_cols_table
        global present_rows_table
        
        pos = int(self.dy_text2.GetValue()) - 1
        buffer_col_val = []
        for i in range(int(self.dy_text2.GetValue()),present_cols_table):
            buffer_col_val.append(frame6.grid.GetColLabelValue(\
                int(i)))

        present_cols_table = present_cols_table - 1
        
        print "buffered val: ",buffer_col_val,pos
        frame6.grid.DeleteCols(pos = pos , numCols = 1)

        count = 0
        for i in range(int(pos),present_cols_table):
            frame6.grid.SetColLabelValue(i,buffer_col_val[count])
            count += 1
        self.Close(True)
        

    def OnSel(self,event):
        global present_cols_table
        global present_rows_table

        self.col_headers = []
        for i in range(present_cols_table):
            self.col_headers.append(frame6.grid.GetColLabelValue(i))

        dlg = wx.SingleChoiceDialog(None,\
        'Select the column on which you want to search',
        'Single Choice',
        self.col_headers,)
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetStringSelection()
            

    def OnGoogle(self,event):
        search_item = self.dy_text2.GetValue()
        Google.main(frame6.comp_name,search_item,self.response,self.col_headers\
                    ,frame6.conn,frame6.c)
        self.Close(True)
               
        
# Class for creating grid and displaying table information            
class CreateGrid(wx.grid.Grid):
    def __init__(self,parent,col_header,cols,all_data,last_view):
        global frame6
        wx.grid.Grid.__init__(self, parent, -1)
        self.CreateGrid(0,cols)
        
        count = 0
        
        if all_data == ():
            d = wx.MessageDialog(self,"Empty Table!!!",\
                             "Message!",wx.OK)
            d.ShowModal()
            self.Close(True)
        else:
            for i in col_header:  #showing column headers in the grid
                self.SetColLabelValue(count,i)
                count += 1
            print "starting ....."
            for count_row in range(len(all_data)):
                self.AppendRows(numRows = 1)
                for count_col in range(cols):
                    #print "Current_row: ",count_row
                    #print "Current_col: ",count_col
                    self.SetCellValue(count_row,count_col,\
                                             all_data[count_row][count_col])
            
        # Now to transfer data to the grid for display
        
        

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,col_headers,all_data,table_name,conn,c,\
                 present_cols_table,present_rows_table,domain,comp_name,last_view):

        self.col_headers = col_headers
        self.all_data = all_data
        self.cols = len(self.col_headers)
        self.table_name = table_name #Company name escaped
        self.conn = conn
        self.c = c
        #self.present_cols_table = present_cols_table
        #self.present_rows_table = present_rows_table
        self.domain_name = domain
        self.comp_name = comp_name # Company name not escaped
        self.last_view = last_view
        
        wx.Frame.__init__(self,parent,id,name,size = (900,600))
        #self.scroll = wx.ScrolledWindow(self, -1)
        #self.scroll.SetScrollbars(1, 1, 600, 400)

        #self.panel = wx.Panel(self)
        self.grid = CreateGrid(self,self.col_headers,\
                               self.cols,self.all_data,self.last_view)

        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()

        # MenuBar for performing table related operations
        filemenu= wx.Menu()
        filemenu.Append(101, "&Add Row","Adding a row")
        filemenu.Append(105, "&Add Column ","Adding a Column")
        filemenu.Append(110, "&Delete Row","Deleting a row")
        filemenu.Append(115, "&Delete Column","Deleting Column")
        filemenu.Append(120, "&Update","Update the Current table")
        filemenu.AppendSeparator()
        filemenu.Append(125,"E&xit"," Terminate the program")

        filemenu1 = wx.Menu()
        filemenu1.Append(130, "&Search Filters","General Searching")

        filemenu2 = wx.Menu()
        filemenu2.Append(135, "&Last Viewed","Last Viewed data andt time")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Operations") # Adding the "filemenu" to the MenuBar
        menuBar.Append(filemenu1,"&Search")
        menuBar.Append(filemenu2,"&Last View")
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        wx.EVT_MENU(self, 101, self.AddRow)
        wx.EVT_MENU(self, 105, self.AddCol)
        wx.EVT_MENU(self, 110, self.DelRow)
        wx.EVT_MENU(self, 115, self.DelCol)
        wx.EVT_MENU(self, 120, self.Update)
        wx.EVT_MENU(self, 125, self.OnExit)
        wx.EVT_MENU(self, 130, self.OnSearch)
        wx.EVT_MENU(self, 135, self.OnLastView)
        

    # Defining menubar functions
    def AddRow(self,event):
        row_frame = PopFrames(None,-6,"Add Rows")
        row_frame.Show(True)
        pass

    def AddCol(self,event):
        col_frame = PopFrames(None,-6,"Add Cols")
        col_frame.Show(True)
        pass

    def DelRow(self,event):
        row_del_frame = PopFrames(None,-6,"Delete Rows")
        row_del_frame.Show(True)
        pass

    def DelCol(self,event):
        col_del_frame = PopFrames(None,-6,"Delete Column")
        col_del_frame.Show(True)
        pass

    def Update(self,event):
        global present_cols_table
        global present_rows_table
        
        # Before updating the company table , we have to first
        # delete the existing company's name.
        #self.table_name = "`"+self.table_name+"`"
        self.domain = "`"+self.domain_name+"`"
        
        d = wx.MessageDialog(self,"Creating backup of the table.In case updating fails,your record will be backed up with extention .bkup ",\
                             "Message",wx.OK)
        d.ShowModal()
        
        self.c.execute('''use %s'''%(self.domain))
        table_bkup = "`"+self.comp_name+".bkup"+"`"
        self.c.execute('''create table %s like %s'''%(table_bkup,self.table_name))
        self.conn.commit()
        
        self.c.execute('''insert into %s select * from %s'''%(table_bkup,self.table_name))
        self.conn.commit()
        
        self.c.execute('''drop table %s'''%(self.table_name))
        self.conn.commit()
        ##
        
        col_header_esc = []
        #print "number of cols: ",present_cols_table
        for i in range(present_cols_table):
            buf_val = self.grid.GetColLabelValue(i)
            buf_val = "`"+buf_val+"`"
            col_header_esc.append(buf_val)
        ret_val = create_table.col_headers(self.conn,self.c,self.domain_name,\
                                           self.table_name,col_header_esc,\
                                           self.comp_name,None)
        if ret_val == 0:
            d = wx.MessageDialog(self,"Error while updating table",\
                             "Warning!",wx.OK)
            d.ShowModal()
        else:
            d = wx.MessageDialog(self,"Table updated",\
                             "Message",wx.OK)
            d.ShowModal()
        

        # Now transferring the data from the grid to database.
        cell_data = []
        #print "present rows update: ",present_rows_table
        for row_count in range(present_rows_table):
            for col_count in range(present_cols_table):
                cell_data.append(frame6.grid.GetCellValue(row_count,col_count))

            ret_val = create_table.enter_data(self.conn,self.c,self.domain_name,\
                                           self.table_name,cell_data,\
                                              self.comp_name)
            cell_data = []
            if ret_val == False:
                    d = wx.MessageDialog(self,"Error while creating table",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                    self.Close(True)
        self.conn.commit()    
        d = wx.MessageDialog(self,"Data entered",\
                             "Message",wx.OK)
        d.ShowModal()
        if ret_val != False:
            self.c.execute('''drop table %s'''%(table_bkup))
            self.conn.commit()
                #self.Close(True)
        self.Close(True)

    def OnSearch(self,event):  # For Searching
        frame = PopFrames(None,-1,"Searching")
        frame.Show(True)

    def OnLastView(self,event):
        d = wx.MessageDialog(None,"This table was last viewed/updated on: %s"\
                             %(self.last_view[0][0]),\
                             "Message",wx.OK)
        d.ShowModal()

    def OnExit(self,event):
        self.Close(True)

    

## Main Function that is first called:
def show_table(conn,c,domain,table_name):

    # table name is not escaped
    
    global frame6
    global present_cols_table
    global present_rows_table

    table_name_esc = "`"+table_name+"`"

    # Show when this table was last viewed in a dialog box
    table_name_comm = "\""+table_name+"\""
    c.execute('''select `last view` from LastView where \
    `Company Name` = %s'''%(table_name_comm))
    last_view = c.fetchall()
    
    
    # Updating the present time in table LastView
    
    #print "table is : ",table_name
    curr_dat_time = "\""+time.ctime()+"\""
    #print curr_dat_time
    c.execute('''update LastView set `last view` = %s where `Company Name` = %s\
    '''%(curr_dat_time,table_name_comm))
    conn.commit()
    ##

    # Show Flag Information if present
    c.execute('''select Flag from LastView where `Company Name` = %s'''\
              %(table_name_comm))
    flag_info = c.fetchall()
    if flag_info[0][0] == u"none":
        pass
    else:
        d = wx.MessageDialog(None,"Flag set by user: %s"%(flag_info[0][0]),"NOTICE!!",wx.OK)
        d.ShowModal()
    
    ##
    c.execute('''show columns from %s'''%(table_name_esc))
    temp = c.fetchall()
    present_cols_table = len(temp) # Very important
                               # maintains no of columns in the table
    #print present_cols_table
    col_headers = []
    for i in range(len(temp)):
        col_headers.append(temp[i][0])
        
    c.execute('''select * from %s'''%(table_name_esc))
    all_data = c.fetchall()
    all_data_new = list(all_data)
    #for i in range(len(all_data)):
    #    all_data_new[i] = list(all_data_new[i])
        
    #for i in range(len(all_data)):
     #   for j in range(present_cols_table):
     #       print i
      #      all_data_new[i][j] = all_data_new[i][j]

    present_rows_table = len(all_data)# Very important
                                      # maintains no of columns in the table 
    #print present_rows_table
    frame6 = CreateFrame(None,-1,"Contents",col_headers,all_data,table_name_esc,\
                         conn,c,present_cols_table,present_rows_table,domain,\
                         table_name,last_view)
    frame6.Show(True)
