# This module is called by "show_database.py".This module basically
# displays all the companys that comes under the major company name.


import wx.grid
import view_info

frame9 = None

class PopFrames(wx.Frame):
    def __init__(self,parent,id,name,conn,c,xtra_info = None):
        self.xtra_info = xtra_info
        if name == "Rename":
            self.count = 0
            wx.Frame.__init__(self,parent,id,name,size = (300,120))
            self.panel = wx.Panel(self)
            self.conn = conn
            self.c = c

            self.st_text2 = wx.StaticText(self.panel,-1,"New Name: ",\
                                    size = (180,-1),pos = (5,45))
            self.dy_text2 = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

            self.button = wx.Button(self.panel,-1,"Rename",pos = (120,80))
            self.Bind(wx.EVT_BUTTON,self.OnRename,self.button)

        elif name == "Notice":
            self.count = 0
            wx.Frame.__init__(self,parent,id,name,size = (300,120))
            self.panel = wx.Panel(self)
            self.conn = conn
            self.c = c

            self.st_text = wx.StaticText(self.panel,-1,"Notice: ",\
                                    size = (180,-1),pos = (5,45))
            self.dy_text = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

            self.button = wx.Button(self.panel,-1,"Flag It",pos = (120,80))
            self.Bind(wx.EVT_BUTTON,self.OnFlagIt,self.button)

        else:
            self.count = 0
            wx.Frame.__init__(self,parent,id,name,size = (300,120))
            self.panel = wx.Panel(self)
            self.conn = conn
            self.c = c

            self.st_text = wx.StaticText(self.panel,-1,"New Name: ",\
                                    size = (180,-1),pos = (5,45))
            self.dy_text = wx.TextCtrl(self.panel,-1,"",pos = (120,45))

            self.button = wx.Button(self.panel,-1,"Copy",pos = (120,80))
            self.Bind(wx.EVT_BUTTON,self.OnCopy,self.button)


    def OnFlagIt(self,event):
        global frame9
        comp_name = self.xtra_info
        comp_name_new = "\""+comp_name+"\""
        notice = self.dy_text.GetValue()
        notice_new = "\""+notice+"\""
        try:
            self.c.execute('''update LastView set Flag = %s where `Company Name` = %s'''\
                       %(notice_new,comp_name_new))
            self.conn.commit()
        except:
            d = wx.MessageDialog(self,"Error while setting the flag",\
                             "Warning!",wx.OK)
            d.ShowModal()
        self.Close(True)

        
    def OnCopy(self,event):
        global frame9
        orig_comp_name = self.xtra_info
        copy_comp_name = self.dy_text.GetValue()

        #First see if the new name follows the naming convention
        self.c.execute('''select * from `MajorName`''')
        majors = self.c.fetchall()

        chk_flag = False
        for i in range(len(majors)):
            buff_len = len(majors[i][0])
            if copy_comp_name[:buff_len]  == majors[i][0]:
                chk_flag = True
                break
            else:
                pass
        if chk_flag == False:
            d = wx.MessageDialog(self,"Naming Convention Not Followed!",\
                             "Warning!",wx.OK)
            d.ShowModal()
            
        else:
            # Check if the company name already exists or not
            self.c.execute('''show tables''')
            data = self.c.fetchall()

            data_new = []
            for i in range(len(data)):
                table = data[i][0]
                l1 = len(table)
                tl1 = l1 -4
                tl2 = l1 - 8
                if table[tl1:] != "Info" and table[tl2:] != "Location":
                    data_new.append(table)
                else:
                    pass
            chk_flag = False
            for i in data_new:
                if i == copy_comp_name:
                    chk_flag = True
                    break
                else:
                    pass
            if chk_flag == True:
                d = wx.MessageDialog(self,"Company already exist!",\
                             "Warning!",wx.OK)
                d.ShowModal()
                

            else: #if company does not exist as this name
                copy_comp_name_new = "`"+copy_comp_name+"`"
                orig_comp_name_new = "`"+orig_comp_name+"`"

                copy_info_tab = "`"+copy_comp_name+"Info"+"`"
                copy_loc_tab = "`"+copy_comp_name+"Location"+"`"

                orig_info_tab = "`"+orig_comp_name+"Info"+"`"
                orig_loc_tab = "`"+orig_comp_name+"Location"+"`"

                last_copy_comp_name = "\""+copy_comp_name+"\""
                
                try:
                    chk_flag = True
                    self.c.execute('''create table if not exists %s like %s'''\
                               %(copy_comp_name_new,orig_comp_name_new))
                    self.conn.commit()
                    self.c.execute('''insert into %s select * from %s '''\
                               %(copy_comp_name_new,orig_comp_name_new))
                    self.conn.commit()

                    self.c.execute('''create table if not exists %s like %s'''\
                                   %(copy_info_tab,orig_info_tab))
                    self.conn.commit()
                    
                    self.c.execute('''insert into %s select * from %s'''\
                                   %(copy_info_tab,orig_info_tab))
                    self.conn.commit()

                    self.c.execute('''create table if not exists %s like %s'''\
                                   %(copy_loc_tab,orig_loc_tab))
                    self.conn.commit()
                    
                    self.c.execute('''insert into %s select * from %s'''\
                                   %(copy_loc_tab,orig_loc_tab))
                    self.conn.commit()

                    self.c.execute('''insert into `LastView` values(%s,"None",u"none")'''\
                                   %(last_copy_comp_name))
                    self.conn.commit()
                except:
                    chk_flag = False
                    d = wx.MessageDialog(self,"Error While Copying!",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                    self.Close(True)

                if chk_flag == True:
                    d = wx.MessageDialog(self,"Successfully completed copying.",\
                             "Message",wx.OK)
                    d.ShowModal()
                    self.Close(True)
            
        

    def OnRename(self,event):
        global frame9
        pr_name = self.xtra_info
        nw_name = self.dy_text2.GetValue()

        self.c.execute('''show tables''')
        data = self.c.fetchall()

        self.c.execute('''select * from `MajorName`''')
        majors = self.c.fetchall()
        
    # From these tables do not show the tables ending with Info and Location.
        data_new = []
        for i in range(len(data)):
            table = data[i][0]
            l1 = len(table)
            tl1 = l1 -4
            tl2 = l1 - 8
            if table[tl1:] != "Info" and table[tl2:] != "Location":
                data_new.append(table)
            else:
                pass
        chk_flag = False
        for i in data_new:
            if i == nw_name:
                chk_flag = True
                break
            else:
                pass
        if chk_flag == True:
            d = wx.MessageDialog(self,"Company already exist!",\
                             "Warning!",wx.OK)
            d.ShowModal()
            self.Close(True)
            
        
        else:
            chk_flag = True
            tl = len(pr_name) - 5
            if pr_name[tl:] == ".bkup":
                # Check if the new company's name follows the standard
                # naming convention.
                if self.count == 0:
                    d = wx.MessageDialog(self,"This chart should be restored to its previous name.Else,would not be accessible",\
                             "Message",wx.OK)
                    d.ShowModal()
                    self.Close(True)
                    
                for i in range(len(majors)):
                    buff_len = len(majors[i][0])
                    if nw_name[:buff_len] == majors[i][0]:
                        chk_flag = False
                        pass
                    else:
                        pass
                if chk_flag == False:
                    pr_name_new = "`"+pr_name+"`"
                    nw_name_new = "`"+nw_name+"`"

                    nw_name_quote = "\""+nw_name+"\""
                    pr_name_quote = "\""+pr_name+"\""
                    try:
                        self.c.execute('''create table %s like %s'''\
                                   %(nw_name_new,pr_name_new))
                        self.conn.commit()
                        self.c.execute('''insert into %s select *  \
                        from %s'''%(nw_name_new,pr_name_new))
                        self.conn.commit()

                        self.c.execute('''update LastView set `Company Name` =%s\
                        where `Company Name` = %s'''%(nw_name_quote,pr_name_quote))
                        self.conn.commit()
                    except:
                        chk_flag = True

                    if chk_flag == True:
                        d = wx.MessageDialog(self,"Renaming Process Failed.Check if any company with same name exists",\
                             "Warning!",wx.OK)
                        d.ShowModal()
                    else:
                        d = wx.MessageDialog(self,"Renaming Process Completed",\
                             "Message",wx.OK)
                        d.ShowModal()
                        self.c.execute('''drop table %s'''%(pr_name_new))
                        self.conn.commit()
                    self.Close(True)
                else:
                    d = wx.MessageDialog(self,"No major name found.Naming convention not followed",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                self.Close(True)

            else:  # If not ".bkup"
                chk_flag = True
                for i in range(len(majors)):
                    buff_len = len(majors[i][0])
                    if nw_name[:buff_len] == majors[i][0]:
                        chk_flag = False
                        pass
                    else:
                        pass
                if chk_flag == False:
                    pr_name_new = "`"+pr_name+"`"
                    nw_name_new = "`"+nw_name+"`"

                    nw_name_quote = "\""+nw_name+"\""
                    pr_name_quote = "\""+pr_name+"\""
                    
                    try:
                        info_tab_pr = "`"+pr_name+"Info"+"`"
                        loc_tab_pr = "`"+pr_name+"Location"+"`"
                        
                        info_tab_new = "`"+nw_name+"Info"+"`"
                        loc_tab_new = "`"+nw_name+"Location"+"`"
                        
                        self.c.execute('''create table %s like %s'''\
                                   %(nw_name_new,pr_name_new))
                        self.conn.commit()
                        
                        self.c.execute('''insert into %s select * \
                            from %s'''%(nw_name_new,pr_name_new))
                        self.conn.commit()

                        self.c.execute('''create table %s like %s'''\
                                       %(info_tab_new,info_tab_pr))
                        self.conn.commit()
                        
                        self.c.execute('''insert into %s select * \
                            from %s'''%(info_tab_new,info_tab_pr))
                        self.conn.commit()

                        self.c.execute('''create table %s like %s'''\
                                       %(loc_tab_new,loc_tab_pr))
                        self.conn.commit()
                        
                        self.c.execute('''insert into %s select * \
                            from %s'''%(loc_tab_new,loc_tab_pr))
                        self.conn.commit()

                        self.c.execute('''update LastView set `Company Name` =%s\
                            where `Company Name` = %s'''%(nw_name_quote,pr_name_quote))
                        self.conn.commit()
                    except:
                        chk_flag = True
                        
                    if chk_flag != True:
                        d = wx.MessageDialog(self,"Renaming Process Completed",\
                           "Message",wx.OK)
                        d.ShowModal()

                        self.c.execute('''drop table %s'''%(pr_name_new))
                        self.conn.commit()
                        self.c.execute('''drop table %s'''%(info_tab_pr))
                        self.conn.commit()
                        self.c.execute('''drop table %s'''%(loc_tab_pr))
                        self.conn.commit()
                        
                        self.Close(True)

                    else:
                        d = wx.MessageDialog(self,"Renaming Process Failed.Check if any company with same name exists",\
                             "Warning!",wx.OK)
                        d.ShowModal()
                    #except:
                        #chk_flag = True

                    #if chk_flag == True:
                    #    d = wx.MessageDialog(self,"Renaming Process Failed.Check if any company with same name exists",\
                    #         "Warning!",wx.OK)
                    #    d.ShowModal()
                    #else:
                    #    d = wx.MessageDialog(self,"Renaming Process Completed",\
                    #         "Message",wx.OK)
                    #    d.ShowModal()
                else:
                    d = wx.MessageDialog(self,"No major name found.Naming convention not followed",\
                             "Warning!",wx.OK)
                    d.ShowModal()
                    self.Close(True)
                
        

class SimpleGrid(wx.grid.Grid):
    def __init__(self,parent,actual_company):
        wx.grid.Grid.__init__(self,parent)

        row = len(actual_company)
        col = 1
        self.CreateGrid(row,col)
        self.SetColLabelValue(0,"Subfolders")

        for i in range(row):
            for j in range(col):
                self.SetCellValue(i,j,actual_company[i])
                

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c,domain_name,\
                 actual_company):
        wx.Frame.__init__(self,parent,id,name,size = (300,400))

        self.actual_company = actual_company
        self.grid = SimpleGrid(self,self.actual_company)
        
        self.conn = conn
        self.c = c
        self.domain_name = domain_name
        
        statusbar = self.CreateStatusBar()
        toolbar = self.CreateToolBar()
        
        filemenu = wx.Menu()
        filemenu.Append(101, "&Info & Employee Details","View Company Information")
        filemenu.Append(130, "&Copy", "Copy the company details with new name")
        filemenu.Append(120, "&Rename","Renames any company name")
        filemenu.AppendSeparator()
        filemenu.Append(125,"E&xit"," Terminate the program")

        
        filemenu1 = wx.Menu()
        filemenu1.Append(135,"&Flag Company","Any Notification about company")
        
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&Details") # Adding the "filemenu" to the MenuBar
        menuBar.Append(filemenu1,"&Flag Info")
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.
        
        wx.EVT_MENU(self, 101, self.ViewInfo)
        wx.EVT_MENU(self, 120, self.Rename)
        wx.EVT_MENU(self, 125, self.OnExit)
        wx.EVT_MENU(self, 130, self.OnCopy)
        wx.EVT_MENU(self, 135, self.OnFlag)

    def ViewInfo(self,event):
        #compiz = PopFrames(None,-7,"Give Details",self.conn,self.c)
        #compiz.Show(True)
        self.sel_comp = None
        for i in range(len(self.actual_company)):
            if self.grid.IsInSelection(i,0):
                self.sel_comp = self.grid.GetCellValue(i,0)
                break
            else:
                pass
        if self.sel_comp == None:
            d = wx.MessageDialog(self,"Select at least one company",\
                             "Warning!",wx.OK)
            d.ShowModal()
        else:
            view_info.show_info(frame9.conn,frame9.c,frame9.domain_name,\
                                self.sel_comp)
        self.Close(True)
            
        
    def Rename(self,event):
        self.sel_comp = None
        for i in range(len(self.actual_company)):
            if self.grid.IsInSelection(i,0):
                self.sel_comp = self.grid.GetCellValue(i,0)
                break
            else:
                pass
        if self.sel_comp == None:
            d = wx.MessageDialog(self,"Select at least one company",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:
            rename = PopFrames(None,-7,"Rename",self.conn,self.c,self.sel_comp)
            rename.Show(True)
            pass
        #self.Close(True)

    def OnCopy(self,event):
        self.sel_comp = None
        for i in range(len(self.actual_company)):
            if self.grid.IsInSelection(i,0):
                self.sel_comp = self.grid.GetCellValue(i,0)
                break
            else:
                pass
        if self.sel_comp == None:
            d = wx.MessageDialog(self,"Select at least one company",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:
            copy = PopFrames(None,-7,"Copy",self.conn,self.c,self.sel_comp)
            copy.Show(True)
            pass
        

    def OnFlag(self,event):
        self.sel_comp = None
        for i in range(len(self.actual_company)):
            if self.grid.IsInSelection(i,0):
                self.sel_comp = self.grid.GetCellValue(i,0)
                break
            else:
                pass
        if self.sel_comp == None:
            d = wx.MessageDialog(self,"Select at least one company",\
                             "Warning!",wx.OK)
            d.ShowModal()

        else:
            Flag = PopFrames(None,-7,"Notice",self.conn,self.c,self.sel_comp)
            Flag.Show(True)
            pass
        #self.Close(True)

    def OnExit(self,event):
        self.Close(True)

def main(conn,c,domain_name,actual_company):
    global frame9

    frame9 = CreateFrame(None,-7,"Company(s)",conn,c,domain_name,\
                         actual_company)
    frame9.Show(True)
