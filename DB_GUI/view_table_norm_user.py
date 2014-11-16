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
        if name == "Searching":
            self.st_text = wx.StaticText(self.panel,-1,"Select Column: ",\
                                         pos = (10,10),size = (180,-1))

            self.button = wx.Button(self.panel,-1,"Select",pos = (150,10))
            self.Bind(wx.EVT_BUTTON,self.OnSel,self.button)

            self.st_text2 = wx.StaticText(self.panel,-1,"Search Box: ",\
                                          pos = (10,65),size = (180,-1))

            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (150,65))
            
            self.button1 = wx.Button(self.panel,-1,"Google",pos = (100,110))
            self.Bind(wx.EVT_BUTTON,self.OnGoogle,self.button1)

            
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
                
            #self.EnableEditing(False)
            print "starting ....."
            for count_row in range(len(all_data)):
                #print count_row
                self.AppendRows(numRows = 1)
                
                for count_col in range(cols):
                    self.SetCellValue(count_row,count_col,\
                                             all_data[count_row][count_col])
                    #self.SetReadOnly(count_row,count_col,isReadOnly=True)
                    #if col_header[count_col] == "Remarks":
                    #    self.SetReadOnly(count_row,count_col,isReadOnly=False)
            print "over...."
            
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

        wx.EVT_MENU(self, 120, self.Update)
        wx.EVT_MENU(self, 125, self.OnExit)
        wx.EVT_MENU(self, 130, self.OnSearch)
        wx.EVT_MENU(self, 135, self.OnLastView)
        

    # Defining menubar functions
    def Update(self,event):
        global present_cols_table
        global present_rows_table

        index_flag_emp = False
        print self.col_headers
        for emp_index in range(int(present_cols_table)):
            if self.col_headers[emp_index] == "Employee ID":
                index_flag_emp = True
                break
            else:
                pass
        if index_flag_emp == False:
            d = wx.MessageDialog(None,"Employee ID column could not be found.Please make a column `Employee ID` and provide the ID's manually",\
                             "Message",wx.OK)
            d.ShowModal()
        
        index_flag_re = False
        for remark_index in range(int(present_cols_table)):
            if self.col_headers[remark_index] == "Remarks":
                index_flag_re = True
                break
            else:
                pass
        if index_flag_re == False:
            d = wx.MessageDialog(None,"`Remarks` column could not be found.Please make a column `Remarks` and provide the ID's manually",\
                             "Message",wx.OK)
            d.ShowModal()
        
        if index_flag_emp == True and index_flag_re == True:
            print "start"
            try:
                # Updating just got faster(Selective updation)
                self.c.execute('''select Remarks from %s'''%(self.table_name))
                all_rmks = self.c.fetchall()
                chged_rmks = []
                for i in range(len(all_rmks)):
                    if all_rmks[i][0] == self.grid.GetCellValue(i,remark_index):
                        pass
                    else:
                        remarks = "\""+self.grid.GetCellValue(i,remark_index)+"\""
                        emp_id = "\""+self.grid.GetCellValue(i,emp_index)+"\""
                        
                        self.c.execute('''update %s set Remarks = %s where `Employee ID`\
                        = %s'''%(self.table_name,remarks,emp_id))
                self.conn.commit()
                        
                error_flag = True
                #for i in range(int(present_rows_table)):
                #    remarks = "\""+self.grid.GetCellValue(i,remark_index)+"\""
                #    emp_id = "\""+self.grid.GetCellValue(i,emp_index)+"\""
                #    self.c.execute('''update %s set Remarks = %s where `Employee ID`\
                #        = %s'''%(self.table_name,remarks,emp_id))
                
                #print "end"
            except:
                error_flag = False
                d = wx.MessageDialog(None,"Error While Updating!!",\
                             "Message",wx.OK)
                d.ShowModal()
        if error_flag == True:
            d = wx.MessageDialog(None,"Table Updated",\
                             "Message",wx.OK)
            d.ShowModal()
        

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
