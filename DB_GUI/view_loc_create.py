# This module creates the location table . This module is called by "view_info.py"
# table:- Comp_nameLocation
# Stores the name of comp,Location,email/url
import wx.grid
import create_table

frame7 = None

present_cols_table1 = None
present_rows_table1 = None

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

        elif name == "view location":
            self.st_text2 = wx.StaticText(self.panel,-1,"Enter Location: ",\
                                        pos = (1,-1),size=(180,-1))
            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (120,-1))

            self.button = wx.Button(self.panel,-1,"Enter",pos = (30,80))
            self.Bind(wx.EVT_BUTTON,self.OnLoc,self.button)

    def OnAddRow(self,event):

        global present_rows_table1
        global present_cols_table1
        
        no_rows = int(self.dy_text.GetValue())
        
        present_rows_table1 = present_rows_table1 + no_rows
        #print "current row count: ",glob_row_count

        frame7.grid.AppendRows(numRows = no_rows)
        self.Close(True)
        pass

    def OnAddCol(self,event):
        # Only one column is allowed to be added at a time for
        # simplicity reasons.
        # "buffer_col_val" is being used because after adding a column
        # from the grid the column headers of all other columns gets changed

        global present_rows_table1
        global present_cols_table1
        
        pos = int(self.dy_text2.GetValue())
        col_name = self.dy_text3.GetValue()

        buffer_col_val = frame7.grid.GetColLabelValue((pos - 1))
        
        
        present_cols_table1 = present_cols_table1 + 1
        
        # if Position field is left blank new column(s) will get
        # appended to the last row in the grid.
        
        if self.dy_text2.GetValue() != "":
            frame7.grid.InsertCols(pos = (pos - 1),numCols = 1)
            frame7.grid.SetColLabelValue(pos,buffer_col_val)
        else:
            frame7.grid.AppendCols(numCols = 1)
            
        frame7.grid.SetColLabelValue((pos-1),col_name)
        self.Close(True)

    def OnDelRow(self,event):
        global present_rows_table1
        global present_cols_table1
        
        pos = int(self.dy_text2.GetValue()) - 1

        present_rows_table1 = present_rows_table1 - 1
        
        no_rows = int(self.dy_text.GetValue())
        frame7.grid.DeleteRows(pos = pos , numRows = no_rows)
        self.Close(True)

    def OnDelCol(self,event):
        
        # Only one column is allowed to be deleted at a time for
        # simplicity reasons.
        # "buffer_col_val" is being used because after deleting a column
        # from the grid the column headers of all other columns gets changed
        global frame7
        global present_rows_table1
        global present_cols_table1
        
        pos = int(self.dy_text2.GetValue()) - 1
        buffer_col_val = []
        for i in range(int(self.dy_text2.GetValue()),present_cols_table1):
            buffer_col_val.append(frame7.grid.GetColLabelValue(\
                int(i)))

        present_cols_table1 = present_cols_table1 - 1
        
        print "buffered val: ",buffer_col_val,pos
        frame7.grid.DeleteCols(pos = pos , numCols = 1)

        count = 0
        for i in range(int(pos),present_cols_table1):
            frame7.grid.SetColLabelValue(i,buffer_col_val[count])
            count += 1
        self.Close(True)
            

class CreateGrid(wx.grid.Grid):
    def __init__(self,parent,col_header_data,cols,all_data):
        
        wx.grid.Grid.__init__(self,parent,-1)
        self.CreateGrid(present_rows_table1,cols)
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

    

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,col_headers,all_data,loc_tab,conn,c,\
                 present_cols_table1,present_rows_table1,comp_name,domain_name):
            
        wx.Frame.__init__(self,parent,id,name,size = (500,700))

        self.conn = conn
        self.c = c
        self.col_headers = col_headers
        self.all_data = all_data
        self.domain_name = domain_name #already escaped in view_info.py
        self.comp_name = comp_name
        self.loc_tab = loc_tab
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
        filemenu.Append(101, "&Add Row","Adding a row")
        filemenu.Append(105, "&Add Column ","Adding a Column")
        filemenu.Append(110, "&Delete Row","Deleting a row")
        filemenu.Append(115, "&Delete Column","Deleting Column")
        filemenu.Append(120, "&Update","Update the Current table")
        filemenu.AppendSeparator()
        filemenu.Append(125,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Operations") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        wx.EVT_MENU(self, 101, self.AddRow)
        wx.EVT_MENU(self, 105, self.AddCol)
        wx.EVT_MENU(self, 110, self.DelRow)
        wx.EVT_MENU(self, 115, self.DelCol)
        wx.EVT_MENU(self, 120, self.Update)
        wx.EVT_MENU(self, 125, self.OnExit)
        

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
        global present_cols_table1
        global present_rows_table1
        
        # Before updating the company table , we have to first
        # delete the existing company's name.
        #self.table_name = "`"+self.table_name+"`"
        #print "creating col. headers"
        if present_rows_table1 == 0:
            d = wx.MessageDialog(self,"Cannot allow to update after deleting the\
                                last row.If updating there should be atleast one row.",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:
            self.c.execute('''use %s'''%(self.domain_name))
        
            d = wx.MessageDialog(self,"Creating backup of the table.In case updating fails,your record will be backed up with extention .bkup ",\
                             "Message",wx.OK)
            d.ShowModal()
        
            loc_bkup = "`"+self.comp_name+"Location"+".bkup"+"`"
            self.c.execute('''create table if not exists %s like %s'''%(loc_bkup,self.loc_tab))
            self.conn.commit()
            
            self.c.execute('''insert into %s select * from %s'''%(loc_bkup,self.loc_tab))
            self.conn.commit()

            self.c.execute('''drop table if exists %s'''%(self.loc_tab))
            self.conn.commit()
            ##
        
            col_header_esc = []
            #print "number of cols: ",glob_col_count
            for i in range(present_cols_table1):
                buf_val = self.grid.GetColLabelValue(i)
                buf_val = "`"+buf_val+"`"
                col_header_esc.append(buf_val)
            
            # Now create the table
            self.c.execute('''create table %s(%s varchar(100))'''\
                       %(self.loc_tab,col_header_esc[0]))
            self.conn.commit()
            for i in col_header_esc[1:]:
                self.c.execute('''alter table %s add column %s varchar(100)'''\
                           %(self.loc_tab,i))
                self.conn.commit()

            # Now add the grid values to the database
            #print "transferring data into database"
            cell_data = []
            #print "no. of rows: ",glob_row_count
            #print "no. of cols: ",glob_col_count
            for i in range(present_rows_table1):
                for j in range(present_cols_table1):
                    cell_data.append(self.grid.GetCellValue(i,j))
                #print "test: ",cell_data
                cell_data = []
        
        
            for row_count in range(present_rows_table1):
                for col_count in range(present_cols_table1):
                    #print col_count
                    #print self.grid.GetCellValue(row_count,col_count)
                    cell_data.append(frame7.grid.GetCellValue(row_count,col_count))
                #print cell_data
                ret_val = create_table.enter_data(self.conn,self.c,self.domain_name,\
                                           self.loc_tab,cell_data,\
                                              self.comp_name)
                cell_data = []
                if ret_val == False:
                    d = wx.MessageDialog(self,"Error while creating Location table",\
                             "Warning!",wx.OK)
                    d.ShowModal()
            
            self.conn.commit()
            if ret_val != False:
                d = wx.MessageDialog(self,"Location table updated",\
                             "Message",wx.OK)
                d.ShowModal()
                self.c.execute('''drop table %s'''%(loc_bkup))
                self.conn.commit()
        #glob_row_count = row_count
        #self.Close(True)

    
    def OnExit(self,event):
        self.Destroy()



def create_loc(conn,c,comp_name,domain_name):
    global frame7
    global present_cols_table1
    global present_rows_table1

    loc_tab = "`"+comp_name+"Location"+"`"

    c.execute('''show columns from %s'''%(loc_tab))
    temp = c.fetchall()
    present_cols_table1 = len(temp) # Very important
                               # maintains no of columns in the table
    #print present_cols_table1
    col_headers = []
    for i in range(len(temp)):
        col_headers.append(temp[i][0])
        
    c.execute('''select * from %s'''%(loc_tab))
    all_data = c.fetchall()

    present_rows_table1 = len(all_data)# Very important
                                      # maintains no of columns in the table 
    #print present_rows_table1
    
    frame7 = CreateFrame(None,-1,"Show/Update Locations(all)",col_headers,all_data,loc_tab,\
                         conn,c,present_cols_table1,present_rows_table1,\
                         comp_name,domain_name)
    frame7.Show(True)
