# This module will prepare the layout for show_database button in
# "user_window"
import wx
import get_grid_info
import get_col_headr_info
import view_table
import view_info
import show_company
import search_company
import wx.grid

frame = None
class FrameSecond(wx.Frame):
    def __init__(self,parent,id,name,operation):
        #time.sleep(2)
        wx.Frame.__init__(self,parent,id,name,size = (380,150))
        panel = wx.Panel(self)
        if operation == "Add":
            self.count_add = 0
            self.text = wx.StaticText(panel,-1,"Name of domain: ",\
                                      size = (180,-1))
            self.dy_text = wx.TextCtrl(panel,-1,"",pos = (120,-1))
            self.button_add = wx.Button(panel,-1,"Enter",pos = (20,70))
            self.Bind(wx.EVT_BUTTON,self.OnAdd,self.button_add)
            self.button_dec = wx.Button(panel,-1,"I decline",pos = (120,70))
            self.Bind(wx.EVT_BUTTON,self.OnDecline,self.button_dec)

        elif operation == "add_table":
            self.count_add_table = 0
            self.text_major = wx.StaticText(panel,-1,"Major Name: ",\
                                           pos = (1,-1),size = (120,-1))
            self.dy_major = wx.TextCtrl(panel,-1,"",pos = (120,-1))
            
            self.text_comp = wx.StaticText(panel,-1,"Company Name: ",\
                                           pos = (1,30),size = (120,-1))
            self.dy_comp = wx.TextCtrl(panel,-1,"",pos = (120,30))
            
            self.text3 = wx.StaticText(panel,-1,"No. of columns: ",\
                                       pos = (1,60),size = (120,-1))
            self.dy_text3 = wx.TextCtrl(panel,-1,"",pos = (120,60))
            
            self.button_tab = wx.Button(panel,-1,"Enter",pos = (250,90))
            self.Bind(wx.EVT_BUTTON,self.OnTable_add,self.button_tab)

        elif operation == "del_table":
            self.count_del_table = 0
            self.text_major = wx.StaticText(panel,-1,"Major Name: ",\
                                           pos = (1,-1),size = (120,-1))
            self.dy_major = wx.TextCtrl(panel,-1,"",pos = (120,-1))
            
            self.text_comp = wx.StaticText(panel,-1,"Company Name: ",\
                                           pos = (1,30),size = (120,-1))
            self.dy_comp = wx.TextCtrl(panel,-1,"",pos = (120,30))
            
            self.button_del = wx.Button(panel,-1,"Delete",pos = (120,70))
            self.Bind(wx.EVT_BUTTON,self.OnTable_del,self.button_del)

        elif operation == "show_company":
            row = range(len(frame.actual_company))
            col = ["Company Name"]
            grid = SimpleGrid(None,frame.actual_company,row,col)
            
        else:
            self.count_del = 0
            self.text1 = wx.StaticText(panel,-1,"Enter Index: ",\
                                       pos = (1,-1),size = (120,-1))
            self.dy_text1 = wx.TextCtrl(panel,-1,"",pos = (80,-1))
            self.text2 = wx.StaticText(panel,-1,"No.of rows: ",\
                                       pos = (1,30),size = (120,-1))
            self.dy_text2 = wx.TextCtrl(panel,-1,"",pos = (80,30))
            self.button_add = wx.Button(panel,-1,"Enter",pos = (20,70))
            self.Bind(wx.EVT_BUTTON,self.OnDel,self.button_add)
            self.button_dec = wx.Button(panel,-1,"I decline",pos = (120,70))
            self.Bind(wx.EVT_BUTTON,self.OnDecline,self.button_dec)

    def OnTable_add(self,event):
        chk_flag = True
        self.no_of_cols = self.dy_text3.GetValue()
        self.comp_name = self.dy_comp.GetValue()

        self.major_name = self.dy_major.GetValue()

        # Check if naming convention has been followed
        if self.comp_name[:len(self.major_name)] != self.major_name:
            chk_flag = False
            f = wx.MessageDialog(self,"Please follow the naming convention.",\
                             "Warning!",wx.OK)
            f.ShowModal()
        
        if chk_flag != False:
            chk_flag = True
            if self.count_add_table == 0:
                d = wx.MessageDialog(self,"Are you sure,you entered the data correctly?",\
                             "Warning!",wx.OK)
                self.count_add_table += 1
                d.ShowModal()
            else:
                if self.no_of_cols == "" or self.comp_name == "":
                    f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                    f.ShowModal()
                else:
                    frame.c.execute('''show tables''')
                    data = frame.c.fetchall()
                
                    for i in range(len(data)):
                        if self.comp_name == data[i][0]:
                            chk_flag = False
                            break
                        else:
                            pass
                    if chk_flag == False:
                        d = wx.MessageDialog(self,"Check if company name already exists",\
                             "Warning!",wx.OK)
                        d.ShowModal()
                        self.Destroy()
                    else:
                        self.comp_name_esc = "`"+self.comp_name+"`"
                        get_col_headr_info.main(self.no_of_cols,self.comp_name_esc,frame.conn,\
                                    frame.c,frame.domain_name,self.comp_name,\
                                            self.major_name)
                        sq = "\""+self.comp_name+"\""+","+"\""+u"none"+"\""\
                         +","+"\""+u"none"+"\""
                    #sq = "\""+self.comp_name+"\""+","+u"none"
                        frame.c.execute('''insert into `LastView`\
                        values(%s)'''%(sq))
                        frame.conn.commit()
                        self.Close(True)
                        pass

    def OnTable_del(self,event):
        print "On delete task"
        self.comp_name = self.dy_comp.GetValue()
        print "company to be deleted: ",self.comp_name
        length = len(self.comp_name)
        tl = length - 5
        c = frame.c
        conn = frame.conn
        self.major_name = self.dy_major.GetValue()

        
        
        if self.count_del_table == 0:
            d = wx.MessageDialog(self,"Are you sure,you entered the data correctly?",\
                             "Warning!",wx.OK)
            self.count_del_table += 1
            d.ShowModal()
        else:
            # Check if major name is written correctly
            c.execute('''select * from MajorName''')
            all_majors = c.fetchall()
            maj_flag = False
            if self.major_name == "":
                f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                f.ShowModal()
            else:
                for i in range(len(all_majors)):
                    if self.major_name == all_majors[i][0]:
                        maj_flag = True
                        break
                    else:
                        pass
                if maj_flag == False:
                    f = wx.MessageDialog(self,"Major Name not found!! ",\
                             "Warning!",wx.OK)
                    f.ShowModal()
            ###

            ##Check if company exists
            c.execute('''show tables''')
            all_comps = c.fetchall()
            
            if self.comp_name == "":
                f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                f.ShowModal()
            else:
                comp_flag = False
                for i in range(len(all_comps)):
                    if self.comp_name == all_comps[i][0]:
                        comp_flag = True
                        break
                    else:
                        pass
                if comp_flag == False:
                    f = wx.MessageDialog(self,"Company not found!!",\
                             "Warning!",wx.OK)
                    f.ShowModal()
                else:
                    if self.comp_name[tl:] != ".bkup":
                        del_major = "\""+self.major_name+"\""
                        c.execute('''show tables''')
                        all_comp = c.fetchall()
                        buf_flag = False
                        count = 0
                        for i in range(len(all_comp)):
                            if all_comp[i][0][:len(self.major_name)] == self.major_name:
                                count = count + 1
                                if count > 3:
                                    buf_flag = True
                                    break
                            else:
                                pass
                        if buf_flag == False:#i.e only one company exists
                            print "In where company does not exists"
                            c.execute('''delete from MajorName where `Company Name` = \
                            %s'''%(del_major))
                            conn.commit()
                            info_tab = "`"+self.comp_name+"Info"+"`"
                            loc_tab = "`"+self.comp_name+"Location"+"`"
                            self.comp_name_esc = "`"+self.comp_name+"`"
                    
                            domain_name_esc = "`"+frame.domain_name+"`"
                            c.execute('''use %s'''%(domain_name_esc))
                            #c.execute('''''')
                            compiz = "\""+self.comp_name+"\""
                            c.execute('''delete from `LastView` where `Company Name`\
                             = %s'''%compiz)
                            conn.commit()
                            c.execute('''drop table if exists %s'''%(info_tab))
                            conn.commit()
                            c.execute('''drop table if exists %s'''%(loc_tab))
                            conn.commit()
                            c.execute('''drop table %s'''%(self.comp_name_esc))
                            conn.commit()
                            row_count = 0
                            col_count = 0
                            while(row_count <= frame.count_comp):
                                val = frame.grid.GetCellValue(row_count,col_count)
                                if val == self.comp_name:
                                    break
                                else:
                                    row_count += 1
                            if row_count != frame.count_comp:
                                frame.grid.DeleteRows(pos = int(row_count),numRows = 1)
                                self.Close()
                            else:
                                f = wx.MessageDialog(self,"Company name not found!!",\
                                 "Warning!",wx.OK)
                                f.ShowModal()
                                print "Not found"
                        else:
                            print "In , when company still exists"
                            info_tab = "`"+self.comp_name+"Info"+"`"
                            loc_tab = "`"+self.comp_name+"Location"+"`"
                            self.comp_name_esc = "`"+self.comp_name+"`"
                    
                            domain_name_esc = "`"+frame.domain_name+"`"
                            c.execute('''use %s'''%(domain_name_esc))
                            #c.execute('''''')
                            compiz = "\""+self.comp_name+"\""
                            c.execute('''delete from `LastView` where `Company Name`\
                             = %s'''%compiz)
                            conn.commit()
                            c.execute('''drop table if exists %s'''%(info_tab))
                            conn.commit()
                            c.execute('''drop table if exists %s'''%(loc_tab))
                            conn.commit()
                            c.execute('''drop table %s'''%(self.comp_name_esc))
                            conn.commit()
                            row_count = 0
                            col_count = 0
                            while(row_count <= frame.count_comp):
                                val = frame.grid.GetCellValue(row_count,col_count)
                                if val == self.comp_name:
                                    break
                                else:
                                    row_count += 1
                            if row_count != frame.count_comp:
                                frame.grid.DeleteRows(pos = int(row_count),numRows = 1)
                                self.Close()
                            else:
                                f = wx.MessageDialog(self,"Company name not found!!",\
                                 "Warning!",wx.OK)
                                f.ShowModal()
                                print "Not found"

                    else:
                        self.comp_name = "`"+self.comp_name+"`"
                        c.execute('''drop table if exists %s'''%(self.comp_name))
                        conn.commit()
                self.Close(True)                        
        
    def OnAdd(self,event):
        domain_name = self.dy_text.GetValue()
        frame.domain_name_esc = "`"+domain_name+"`"
        chk_flag = True
        if self.count_add == 0:
            d = wx.MessageDialog(self,"Are you sure,you want to add the database.Please check the domain name",\
                             "Warning!",wx.OK)
            self.count_add += 1
            d.ShowModal()
        else:
            if domain_name == "":
                f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                f.ShowModal()
            else:
                try:
                    frame.c.execute('''create database %s'''%(frame.domain_name_esc))
                    frame.conn.commit()
                except:
                    chk_flag = False
                    d = wx.MessageDialog(self,"Check if database name already exists",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                frame.c.execute('''use %s'''%(frame.domain_name_esc))
                frame.c.execute('''show tables''')
                all_tables = frame.c.fetchall()
                chk_flag_x = True
                for i in range(len(all_tables)):
                    if all_tables[i][0] == "LastView":
                        chk_flag_x = False
                        break
                    else:
                        pass
                if chk_flag_x == True:
                    frame.c.execute('''create table `LastView`(`Company Name`\
                        varchar(65),`last view` varchar(65),Flag varchar(200))''')
                    frame.conn.commit()

                chk_flag1_x = True
                for i in range(len(all_tables)):
                    if all_tables[i][0] == "MajorName":
                        chk_flag1_x = False
                        break
                    else:
                        pass
        
                if chk_flag1_x == True:
                    c.execute('''create table `MajorName`(`Company Name`\
                        varchar(65))''')
                    conn.commit()

                    
                if chk_flag == True:
                    [data,count_row] = get_grid_info.main(frame.conn,frame.c,\
                                                          "show_database")
                    # Gets number of rows presently there in the database
                    frame.grid.AppendRows(numRows = 1)
                    print count_row
                    frame.grid.SetCellValue(int(len(count_row))- 1,0,domain_name)
                    self.Close()
                else:
                    self.Destroy()

    def OnDel(self,event):
        del_database = [] # list containing all the databases that needs to be dropped
        if self.count_del == 0:
            d = wx.MessageDialog(self,"Are you sure,you want to delete the database.Please check the index number.",\
                             "Warning!",wx.OK)
            self.count_del += 1
            d.ShowModal()
        else:
            get_index = self.dy_text1.GetValue()
            get_rows = self.dy_text2.GetValue()

            if get_index == "" or get_rows == "":
                f = wx.MessageDialog(self,"Do not leave the text box blank",\
                             "Warning!",wx.OK)
                f.ShowModal()
            else:
                
                index_list = range(int(get_rows))
                print index_list
        
                for j in range(len(index_list)):
                    del_database.append(frame.grid.GetCellValue((int(get_index)+index_list[j]-1),0))
                print del_database
                
                for j in range(len(del_database)):
                    del_database[j] = "`"+del_database[j]+"`"
                    print del_database[j]
                    frame.c.execute('''drop database %s'''%str(del_database[j]))
                    frame.conn.commit()
                frame.grid.DeleteRows(pos = int(get_index)-1,numRows = int(get_rows))
                self.Close()

    def OnDecline(self,event):
        self.Destroy()
        
class SimpleGrid(wx.grid.Grid):
    def __init__(self, parent,data,row,col):
        wx.grid.Grid.__init__(self, parent, -1)
        no_col = len(col)
        no_row = len(row)
        self.CreateGrid(no_row,no_col)
        self.SetColLabelValue(0,col[0])
        count = 0
        for i in range(no_row):
            #self.SetRowLabelValue(i,"")
            count += 1
            for j in range(no_col):
                #self.SetCellValue(i,j,data[i])
                self.SetCellValue(i,j,data[i])
                print data[i]
                
        #tableBase = generictable.GenericTable(data,row,col)
        #self.SetTable(tableBase)

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c):
        self.conn = conn
        self.c = c
        self.tables_count = 0

        wx.Frame.__init__(self,parent,id,name,size = (1000,1000))
        # Creating Splitter Window
        self.initpos = 400
                                                    
        self.sp = wx.SplitterWindow(self)
        self.p1 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        self.p1.SetBackgroundColour("light blue")
                                                                            
        self.p2 = wx.Panel(self.sp, style=wx.SUNKEN_BORDER)
        self.p2.SetBackgroundColour("light blue")

        self.sp.Initialize(self.p1)
        self.sp.Initialize(self.p2)                                      
        self.sp.SetMinimumPaneSize(10)
        self.sp.SplitVertically(self.p1, self.p2,self.initpos)

        #image = wx.Image("/home/arun/Download/Feodora.bmp", wx.BITMAP_TYPE_BMP)
        #bmp = image.ConvertToBitmap()
        #sb1 = wx.StaticBitmap(self.p1, -1, wx.BitmapFromImage(image))
        ##
        #panel = wx.Panel(self)

        # Creating Buttons for panel1
        self.button1 = wx.Button(self.p1,-1," Add Dbase ")
        self.Bind(wx.EVT_BUTTON,self.OnClick1,self.button1)

        self.button2 = wx.Button(self.p1,-1,"Delete Dbase")
        self.Bind(wx.EVT_BUTTON,self.OnClick2,self.button2)

        self.button3 = wx.Button(self.p1,-1," Show Table ")
        self.Bind(wx.EVT_BUTTON,self.OnClick3,self.button3)

        self.button4 = wx.Button(self.p1,-1,"   Close    ")
        self.Bind(wx.EVT_BUTTON,self.OnClick4,self.button4)

        
        # Pass it to grid

        [data,row] = get_grid_info.main(self.conn,self.c,"show_database")
        col = ["Domains"]
        data = tuple(data)
        row = tuple(row)
        col = tuple(col)
        self.grid = SimpleGrid(self.p1,data,row,col)
        #self.grid.AppendRows(numRows = 1)

        # Sizers
        sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        sizer.AddMany([self.button1,self.button2,self.button3,self.button4,\
                           self.grid])
        self.p1.SetSizer(sizer)



    def OnClick1(self,event):  # Add dbase
        self.frame2 = FrameSecond(None,-2,"Add/Delete Dbase","Add")
        self.frame2.Show(True)
        pass

    def OnClick2(self,event):  # Delete Dbase
        self.frame2 = FrameSecond(None,-3,"Add/Delete Dbase","Del")
        self.frame2.Show(True)
        #self.c.execute('''drop database''')
        pass

    def OnClick3(self,event):  # Show Table
        #frame.grid.SelectCol(0, addToSelected=False)
        self.index = []
        if self.tables_count == 0:
            self.tables_count += 1 
            # Creating Buttons for panel 2
            # These buttons will do operations related to table/company-name

            self.button1_2 = wx.Button(self.p2,-1," Add Company ")
            self.Bind(wx.EVT_BUTTON,self.OnClick1_2,self.button1_2)

            self.button2_2 = wx.Button(self.p2,-1,"Delete Company")
            self.Bind(wx.EVT_BUTTON,self.OnClick2_2,self.button2_2)

            self.button3_2 = wx.Button(self.p2,-1,"View Company(s)")
            self.Bind(wx.EVT_BUTTON,self.OnClick3_2,self.button3_2)

            self.button4_2 = wx.Button(self.p2,-1,"Search Company")
            self.Bind(wx.EVT_BUTTON,self.OnClick4_2,self.button4_2)
        
        else:
            self.grid1.Destroy()
        # Prepare grid    
        [data,rows] = get_grid_info.main(self.conn,self.c,"show_database")
        self.index = []
        for i in range(len(rows)):
            if frame.grid.IsInSelection(i,0):
                self.index.append(i)
                print "yes"+ str(i)
            else:
                pass
        if self.index == []:
            d = wx.MessageDialog(self,"Please Select Any Database",\
                             "Message",wx.OK)
            d.ShowModal()
            pass
        else:
            self.domain_name = frame.grid.GetCellValue(self.index[0],0)
            self.domain = "`"+self.domain_name+"`"
            frame.c.execute('''use %s'''%(self.domain))
            frame.c.execute('''select * from `MajorName`''')
            major_table = frame.c.fetchall()
            major = []
            for i in range(len(major_table)):
                major.append(major_table[i][0])
            [tables,count_comp] = get_grid_info.tables(frame.conn,frame.c,\
                                                   self.domain_name)
            self.tables = tables
            self.major_tab = major_table
            row = tuple(range(len(tables)))
            self.row = tuple(range(len(major_table)))
            col = ["Company"]
            col  = tuple(col)
            frame.count_comp = count_comp # Number of companie in the database
            #self.grid1 = SimpleGrid(self.p2,tables,row,col)
            self.grid1 = SimpleGrid(self.p2,major,self.row,col)
            #Sizer
            sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
            sizer.AddMany([self.button1_2,self.button2_2,self.button3_2,\
                       self.button4_2,self.grid1])
            self.p2.SetSizer(sizer)
        
    def OnClick4(self,event):  # Close
        self.Destroy()
        pass

    # Functions for buttons in panel 2

    def OnClick1_2(self,event): # Add Company to the table
        self.frame3 = FrameSecond(None,-3,"Add Table","add_table")
        self.frame3.Show(True)
        pass

    def OnClick2_2(self,event): # Delete Company from the table
        self.frame4 = FrameSecond(None,-4,"Delete Table","del_table")
        self.frame4.Show(True)
        pass

    def OnClick3_2(self,event): # Shows the contents of the selected tables
        self.index2_table = []
        for i in range(len(self.row)):
            if frame.grid1.IsInSelection(i,0):
                self.index2_table.append(i)
                #print "yes"+ str(i)
            else:
                pass
        if self.index2_table == []:
            d = wx.MessageDialog(self,"Please Select Any Company",\
                             "Message",wx.OK)
            d.ShowModal()
            pass
        else:
            major_name_selected = frame.grid1.GetCellValue(self.index2_table[0],0)
            #print major_name_selected
            frame.c.execute('''show tables''')
            length_company = len(major_name_selected)
            all_company = frame.c.fetchall()
            
            frame.c.execute('''select * from `MajorName`''')
            all_majors = frame.c.fetchall()
                            
            print all_company
            frame.actual_company = []
            for i in range(len(all_company)):
                if all_company[i][0][:length_company] == major_name_selected:
                    tl1 = len(all_company[i][0]) -4
                    tl2 = len(all_company[i][0]) - 8
                    if all_company[i][0][tl1:] != "Info" and\
                         all_company[i][0][tl2:] != "Location":
                        frame.actual_company.append(all_company[i][0])
                    else:
                        pass
            #print "Showing Frame"
            #print frame.actual_company

            show_company.main(frame.conn,frame.c,frame.domain_name,frame.actual_company)
        #frame9 = FrameSecond(None,-1,"Companies","show_company")
        #frame9.Show(True)
        
        
        #self.index1_table = []
        #[tables,no_tables] = get_grid_info.tables(frame.conn,frame.c,\
                                                  #frame.domain_name)
        #print "tables",tables
        #print "no tables",no_tables
        #for i in range(no_tables):
        #    if frame.grid1.IsInSelection(i,0):
        #        self.index1_table.append(i)
        #        print "yes"+ str(i)
        #    else:
        #        pass
        #table_name = frame.grid1.GetCellValue(self.index1_table[0],0)
        #print "selected table is",table_name
        #print "database is",frame.domain_name
        
        #view_info.show_info(frame.conn,frame.c,frame.domain_name,table_name)
        
        #view_table.show_table(frame.conn,frame.c,frame.domain_name,table_name)

    def OnClick4_2(self,event): # Search Company
        search_company.main(frame.conn,frame.c,frame.domain_name)
    
def main(conn,c):
    global frame
    frame = CreateFrame(None,-1,"Show Database",conn,c)
    frame.Show(True)
