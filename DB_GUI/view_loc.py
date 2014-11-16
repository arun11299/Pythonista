# This module creates the table for viewing the locations where the company is
# present.This module is called by "view_info.py"
# "view_info.py" takes the country's name and this module displays only
# the locations within the country.

import wx.grid
frame8 = None


class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,data,no_cols,col_headers):
        global frame8
        wx.grid.Grid.__init__(self,parent,-1)
        
        rows = len(data)
        self.CreateGrid(0,no_cols)
        count = 0
        if data == ():
            d = wx.MessageDialog(self,"Empty Table!!!",\
                             "Message!",wx.OK)
            d.ShowModal()
        else:
            for i in col_headers:  #showing column headers in the grid
                self.SetColLabelValue(count,i)
                count += 1
            for count_row in range(rows):
                self.AppendRows(numRows = (count_row + 1))
                for count_col in range(no_cols):
                    self.SetCellValue(count_row,count_col,\
                                             data[count_row][count_col])
                    print self.GetCellValue(count_row,count_col)
            print "table has been displayed"
            print "no of rows",count_row

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,country_index,loc_tab,no_cols,col_headers,\
                 country_name,c,conn):
        wx.Frame.__init__(self,parent,id,size = (400,600))
        self.c = c
        self.conn = conn
        self.country_index = country_index
        self.loc_tab = loc_tab
        self.no_cols = no_cols
        self.col_headers = col_headers
        self.country_name = "\""+country_name+"\""

        self.c.execute('''select * from %s where Country = %s'''\
                       %(self.loc_tab,self.country_name))
        data = self.c.fetchall()

        self.grid = SimpleGrid(self,data,self.no_cols,self.col_headers)
        
def show_locations(conn,c,comp_name,country_name):
    global frame8
    loc_tab = "`"+comp_name+"Location"+"`"
    c.execute('''show columns from %s'''%(loc_tab))
    col_headers_all = c.fetchall()
    col_headers = []
    country_index = None
    no_cols = len(col_headers_all)
    for i in range(no_cols):
        col_headers.append(col_headers_all[i][0])
    for i in range(no_cols):
        if col_headers[i][0] == country_name:
            country_index = i
            break
        else:
            country_index = None
            pass

    frame8 = CreateFrame(None,-1,"Show Locations(Filtered)",country_index,loc_tab,no_cols,\
                         col_headers,country_name,c,conn)
    frame8.Show(True)
    
