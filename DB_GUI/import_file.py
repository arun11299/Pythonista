# This module is for importing database from *.xls file
import wx
import time
import cr_dbase
import os

class CreateFrame(wx.Frame):
    def __init__(self,parent,id,name,conn,c):
        # Required for Python-MySQL API
        self.conn = conn
        self.c = c
        
        wx.Frame.__init__(self,None,id,name,size = (550,300))
        panel = wx.Panel(self)
        self.CreateStatusBar()
        # Domain
        self.st_text_domain = wx.StaticText(panel,-1,"Enter Domain: ",pos = (5,-1))
        self.dy_text_domain = wx.TextCtrl(panel,-1,"",size = (200,-1),pos = (175,-1))

        self.button2 = wx.Button(panel,-1,"Select",pos = (380,-1))
        self.Bind(wx.EVT_BUTTON,self.OnSelect,self.button2)
        # Name Of Root Company(Major name)
        self.st_major = wx.StaticText(panel,-1,"Enter Major Name: ",pos = (5,45))
        self.dy_major = wx.TextCtrl(panel,-1,"",size = (200,-1),pos = (175,45))

        # Company
        self.st_company = wx.StaticText(panel,-1,"Enter name of company: ",pos = (5,90))
        self.dy_company = wx.TextCtrl(panel,-1,"",size = (200,-1),pos = (175,90))

        # Path to the file
        self.st_filepath = wx.StaticText(panel,-1,"Path: ",pos = (5,135))
        self.dy_filepath = wx.TextCtrl(panel,-1,"",size = (200,-1),pos = (175,135))
        # Attach File
        self.button1 = wx.Button(panel,-1,"Attach File",pos = (380,135))
        self.Bind(wx.EVT_BUTTON,self.OnAttach,self.button1)

        # Name of the file
        self.st_name = wx.StaticText(panel,-1,"File name: ",pos = (5,180))
        self.dy_name = wx.TextCtrl(panel,-1,"",size = (200,-1),pos = (175,180))

        # Import Button
        self.button = wx.Button(panel,-1,"Import",pos = (175,215))
        self.Bind(wx.EVT_BUTTON,self.OnClick,self.button)

        # MenuBar
        filemenu= wx.Menu()
        filemenu.Append(101, "&Open"," selects file")
        filemenu.AppendSeparator()
        filemenu.Append(105,"E&xit"," Terminate the program")
        # Creating the menubar.
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu,"&File") # Adding the "filemenu" to the MenuBar
        self.SetMenuBar(menuBar) # Adding the MenuBar to the Frame content.

        wx.EVT_MENU(self, 101, self.OnOpen)
        wx.EVT_MENU(self, 105, self.OnExit)

        # Sizers
        #sizer = wx.FlexGridSizer(cols=2, hgap=6, vgap=6)
        #sizer.AddMany([self.st_text_domain,self.dy_text_domain,self.st_major,\
        #               self.dy_major,self.st_company,\
        #               self.dy_company,self.st_filepath,self.dy_filepath,\
        #               self.st_name,self.dy_name,self.button])
        #panel.SetSizer(sizer)


    def OnSelect(self,event):
        self.c.execute('''show databases''')
        buff_dbase = self.c.fetchall()
        all_dbase = []

        for i in range(len(buff_dbase)):
            if (buff_dbase[i][0] != "information_schema")\
               and (buff_dbase[i][0] != "test") and (buff_dbase[i][0] != "mysql"):
                all_dbase.append(buff_dbase[i][0])

        dlg = wx.SingleChoiceDialog(None,\
        'Select the domain::',
        'Single Choice',
        all_dbase,)
        if dlg.ShowModal() == wx.ID_OK:
            self.response = dlg.GetStringSelection()
            self.dy_text_domain.SetValue(self.response)

    def OnClick(self,event):
        chk_flag = True
        
        domain = self.dy_text_domain.GetValue()
        major_name = self.dy_major.GetValue()
        company = self.dy_company.GetValue()

        if company[:len(major_name)] != major_name:
            chk_flag = False
            f = wx.MessageDialog(self,"Please follow the naming convention.",\
                             "Warning!",wx.OK)
            f.ShowModal()
            
        if chk_flag != False:
            chk_flag = True
            file_name = self.dy_name.GetValue()
            dir_name = self.dy_filepath.GetValue()

        
            for trace in (domain,major_name,company,file_name,dir_name):
                if trace == '':
                    chk_flag = False
                    break
                else:
                    pass
            if chk_flag == True:
                ret_val = cr_dbase.create_database(self.conn,self.c,domain,company,file_name,\
                                    dir_name,major_name)
                if ret_val == 1:
                    d = wx.MessageDialog(self,"Your database have been transfered",\
                                 "Congrats!!!",wx.OK)
                    d.ShowModal()
                else:
                    d = wx.MessageDialog(self,"Error while transffering database.Please check if the same company exists in your present data base",\
                                 "Warning!!!",wx.OK)
                    d.ShowModal()
                self.Close()

            else:
                d = wx.MessageDialog(self,"Blank spaces does'nt look good.So,fill in something.",\
                                 "Warning!!!",wx.OK)
                d.ShowModal()

    def OnExit(self,event):
        self.Close(True)

    def OnOpen(self,event):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            #print self.filename
            self.dy_name.SetValue(self.filename)
            
            self.dirname=dlg.GetDirectory()
            #print self.dirname
            self.dy_filepath.SetValue(self.dirname)
            
            #print os.getcwd()
            #self.path = dlg.GetPath()
            #print self.path

            #f=open(os.path.join(self.dirname,self.filename),'r')
            #self.control.SetValue(f.read())
            #f.close()

        dlg.Destroy()

    def OnAttach(self,event):
        """ Open a file"""
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename=dlg.GetFilename()
            #print self.filename
            self.dy_name.SetValue(self.filename)
            
            self.dirname=dlg.GetDirectory()
            #print self.dirname
            self.dy_filepath.SetValue(self.dirname)
            
            #print os.getcwd()
        pass

def main(conn,c):
    frame = CreateFrame(None,-1,"Import",conn,c)
    frame.Show(True)
