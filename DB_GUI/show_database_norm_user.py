# This module will prepare the layout for show_database button in
# "user_window"
import wx
import get_grid_info
import get_col_headr_info
#import view_table
#import view_info_norm_user
import show_company_norm_user
import search_company_norm_user
import wx.grid

frame = None
class FrameSecond(wx.Frame):
    def __init__(self,parent,id,name,operation):
        #time.sleep(2)
        wx.Frame.__init__(self,parent,id,name,size = (380,150))
        panel = wx.Panel(self)
        if operation == "show_company":
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
        sizer.AddMany([self.button3,self.button4,\
                           self.grid])
        self.p1.SetSizer(sizer)



    def OnClick3(self,event):  # Show Table
        #frame.grid.SelectCol(0, addToSelected=False)
        self.index = []
        if self.tables_count == 0:
            self.tables_count += 1 
            # Creating Buttons for panel 2
            # These buttons will do operations related to table/company-name

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
            sizer.AddMany([self.button3_2,\
                       self.button4_2,self.grid1])
            self.p2.SetSizer(sizer)
        
    def OnClick4(self,event):  # Close
        self.Destroy()
        pass

    # Functions for buttons in panel 2

    def OnClick3_2(self,event): # Shows the contents of the selected tables
        self.index2_table = []
        for i in range(len(self.row)):
            if frame.grid1.IsInSelection(i,0):
                self.index2_table.append(i)
                print "yes"+ str(i)
            else:
                pass
        if self.index2_table == []:
            d = wx.MessageDialog(self,"Please Select Any Company",\
                             "Message",wx.OK)
            d.ShowModal()
            pass
        else:
            major_name_selected = frame.grid1.GetCellValue(self.index2_table[0],0)
            print major_name_selected
            frame.c.execute('''show tables''')
            length_company = len(major_name_selected)
            all_company = frame.c.fetchall()
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
            print "Showing Frame"
            print frame.actual_company

            show_company_norm_user.main(frame.conn,frame.c,frame.domain_name,frame.actual_company)
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
        search_company_norm_user.main(frame.conn,frame.c,frame.domain_name)
    
def main(conn,c):
    global frame
    frame = CreateFrame(None,-1,"Show Database",conn,c)
    frame.Show(True)
