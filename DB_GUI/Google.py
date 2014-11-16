# This module does the computations required for searching. This module is
# called by view_table.py.

import wx.grid
class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,all_sel_col_data,col_headers):
        wx.grid.Grid.__init__(self,parent)
        self.CreateGrid(0,len(col_headers))

        for i in range(len(col_headers)):
            self.SetColLabelValue(i,col_headers[i])

        #self.EnableEditing(False)
        
        for i in range(len(all_sel_col_data)):
            self.AppendRows(numRows = 1)
            for j in range(len(col_headers)):
                self.SetCellValue(i,j,all_sel_col_data[i][0][j])
                if col_headers[j] != "Remarks":
                    self.SetReadOnly(i,j,isReadOnly=True)
                else:
                    self.SetReadOnly(i,j,isReadOnly=False)
        

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,all_sel_col_data,col_headers,matching_data,\
                 comp_name,conn,c):
        wx.Frame.__init__(self,parent,id,name,size = (900,600))
        
        self.all_sel_col_data = all_sel_col_data
        self.col_headers = col_headers
        self.matching_data = matching_data
        self.comp_name = comp_name
        self.conn = conn
        self.c = c
        
        if matching_data == []:
            d = wx.MessageDialog(self,"No Search Results Found",\
                             "Message",wx.OK)
            d.ShowModal()
            self.Close(True)
        self.grid = SimpleGrid(self,all_sel_col_data,col_headers)

        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()

        # MenuBar for performing table related operations
        filemenu= wx.Menu()
        filemenu.Append(101, "&Update","Update the search result")
        filemenu.AppendSeparator()
        filemenu.Append(105, "E&xit", "Terminate this window")
        
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Operations") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        wx.EVT_MENU(self, 101, self.Update)
        wx.EVT_MENU(self, 105, self.OnExit)


    def Update(self,event):
        flag = None
        d = wx.MessageDialog(self,"Perform updation?",\
                             "Message",wx.OK)
        d.ShowModal()

        comp_name_esc = "`"+self.comp_name+"`"
        col_header = "`"+self.col_headers[0]+"`"
        
        flag = False       
        for i in range(len(self.all_sel_col_data)):
            #default_col_val = "\""+self.grid.GetCellValue(i,0)+"\""
            for j in range(len(self.col_headers)):
                if self.col_headers[j] == "Remarks":
                    flag = True
                    break
                else:
                    pass
            if flag == True:
                update_val = "\""+self.grid.GetCellValue(i,j)+"\""
            else:
                d = wx.MessageDialog(self,"Remarks column could not be found",\
                             "Message",wx.OK)
                d.ShowModal()
                
            flag = False
            for j in range(len(self.col_headers)):
                if self.col_headers[j] == "Employee ID":
                    flag = True
                    break
                else:
                    pass
            if flag == True:
                emp_val = "\""+self.grid.GetCellValue(i,j)+"\""
            else:
                d = wx.MessageDialog(self,"`Employee ID` column could not be found",\
                             "Message",wx.OK)
                d.ShowModal()
            try:
                self.c.execute('''update %s set Remarks = %s where `Employee ID` = %s'''\
                           %(comp_name_esc,update_val,\
                             emp_val))
                #self.conn.commit()
            except:
                flag = False
                d = wx.MessageDialog(self,"Could not update.Sorry!",\
                             "Message",wx.OK)
                d.ShowModal()
                
        self.conn.commit()
        if flag != False:
            d = wx.MessageDialog(self,"Updated.",\
                             "Message",wx.OK)
            d.ShowModal()
            
            
        pass
    
    def OnExit(self,event):
        self.Destroy()
        pass
        

def main(comp_name,search_item,response,col_headers,conn,c):
    col_selected = response
    col_selected_esc = "`"+col_selected+"`"

    comp_name_esc = "`"+comp_name+"`"
    
    length = len(search_item)
    list_search_item = list(search_item)
    
    c.execute('''select %s from %s'''%(col_selected_esc,comp_name_esc))
    conn.commit()
    sel_col_data = c.fetchall()
    
    if list_search_item.pop() == "*":  # if * is used
        
        search_item_new = search_item[:(length - 1)]
        length = len(search_item_new)
        matching_data = []

        count = 0
        for i in range(len(sel_col_data)):
            if sel_col_data[i][0][:length] == search_item_new:
                if count == 0:
                    matching_data.append(sel_col_data[i][0])
                    count += 1
                else:
                    chk_flag = True
                    for j in matching_data:
                        if j == sel_col_data[i][0]:
                            chk_flag = False
                            break
                        else:
                            pass
                    if chk_flag == True:
                        matching_data.append(sel_col_data[i][0])

        else:
            all_sel_col_data = []
            for i in range(len(matching_data)):
                matched_data = "\""+matching_data[i]+"\""
                c.execute('''select * from %s where %s = %s'''%(comp_name_esc,\
                                                        col_selected_esc,\
                                                        matched_data))
                conn.commit()
            
                buf_list = c.fetchall()
                all_sel_col_data.append(buf_list)
                # all_sel_col[list_index][tuple_index][0]

            frame14 = CreateFrame(None,-1,"Searched Data",all_sel_col_data,\
                              col_headers,matching_data,comp_name,conn,c)
            frame14.Show(True)


    else:  # if absolute data put that is no trailing *
        count = 0
        matching_data = []
        for i in range(len(sel_col_data)):
            if sel_col_data[i][0][:length] == search_item:
                if count == 0:
                    matching_data.append(sel_col_data[i][0])
                    count += 1
                else:
                    chk_flag = True
                    for j in matching_data:
                        if j == sel_col_data[i][0]:
                            chk_flag = False
                            break
                        else:
                            pass
                    if chk_flag == True:
                        matching_data.append(sel_col_data[i][0])

        
        else:
            all_sel_col_data = []
            for i in range(len(matching_data)):
                matched_data = "\""+matching_data[i]+"\""
                c.execute('''select * from %s where %s = %s'''%(comp_name_esc,\
                                                        col_selected_esc,\
                                                        matched_data))
                conn.commit()
            
                buf_list = c.fetchall()
                all_sel_col_data.append(buf_list)
                # all_sel_col[list_index][tuple_index][0]

            frame14 = CreateFrame(None,-1,"Searched Data",all_sel_col_data,\
                              col_headers,matching_data,comp_name,conn,c)
            frame14.Show(True)
        




            
        
