# This Module will read from the excel sheet
import xlrd
import merge
import time
import wx

        
def transfer(c,conn,file_name,company_table_merged,domain,company,major_name):
    count_rows = 0
    count_cols = 0
    flag = False
    try:
        work_book = xlrd.open_workbook(file_name)
    except IOError:
        d = wx.MessageDialog(None,"File does not exist! ",\
                             "Warning",wx.OK)
        d.ShowModal()
        #print "File Does Not Exist"
        #print "Check File Name Carefully"
    sheet = work_book.sheet_names()
    #print "sheet name is: "+str(sheet[0])
    try:
        for i in range(len(sheet)):
            sh = work_book.sheet_by_name(sheet[i])
            rows = sh.nrows
            if rows !=0:
                break
            else:
                pass
    except XLRDError:
        d = wx.MessageDialog(None,"No Sheet found!!",\
                             "Warning",wx.OK)
        d.ShowModal()
        #print "No Sheet Found!"
    rows = sh.nrows
    #print "Number Of Rows: "+str(rows)
    cols  = sh.ncols
    #print "Number Of Columns: "+str(cols)

    # Now Read the Excel Sheet
    # Problem 1: Check from where the row starts
    # Problem 2: Blank columns and rows should not be included in the database

    for count_rows in range(rows):
        row_list = sh.row_values(count_rows)
        for i in range (cols):
            if row_list[i] != '':
                flag = True
                break
            else:
                pass
        if flag == True: #Means valid row found
            break
        else:
            pass

    # Valid row found

    first_row_val = sh.row_values(count_rows)
    
    # MySQL cannot take database name,table and member name as
    # two words seperated by space.
    #merged_first_row_val = merge.split_merge(first_row_val)
    merged_first_row_val = first_row_val
    print "length of merged: "+str(len(merged_first_row_val))
    # Find the blank columns in the first row
    index_of_valid_col = []
    for i in range(cols):
        if first_row_val[i] != '':
            index_of_valid_col.append(i)
        else:
            pass

    print index_of_valid_col
    table_contents = []
    for i in index_of_valid_col:
        table_contents.append(merged_first_row_val[i])

    # Dealing with space at last place
    #print "blank"
    #print table_contents
    for i in range(len(table_contents)):
        buf = table_contents[i]
        if isinstance(buf,unicode):
            buf_list = list(table_contents[i])
            if buf_list.pop() == " ":
                #print "found blnk"
                table_contents[i] = table_contents[i][:(len(table_contents[i]) - 1)]
            else:
                pass
        
    #print table_contents
    ## To include special characters (&,%,$,@) in the column name
    ## warp the string inside `string`
        
    for z in range(len(table_contents)):
            temp = str(table_contents[z])
            temp = "`"+temp+"`"
            table_contents[z] = temp
            
    # Now create table
    c.execute('''use %s'''%domain)
    #print table_contents

   
    # Putting the major_name of company into table called MajorName
    # Check if major name already exists in the table
    # if exists do not enter it again
    c.execute('''select * from `MajorName`''')
    major_table_name = c.fetchall()
    buf_flag = True
    if major_table_name != ():
        for i in range(len(major_table_name)):
            if major_table_name[i][0] == major_name:
                buf_flag = False
                break
            else:
                pass
        if buf_flag == True:
            major_name = "\""+major_name+"\""
            c.execute('''insert into `MajorName` values(%s)'''%(major_name))
            conn.commit()
        else:
            pass
    else:
        major_name = "\""+major_name+"\""
        c.execute('''insert into `MajorName` values(%s)'''%(major_name))
        conn.commit()

    # Putting the company's name into table LastView
    #buff = "\""+company+"\""+","+"\""+"none"+"\""
    buff = "\""+company+"\""+","+"\""+u"none"+"\""+","+"\""+u"none"+"\""
    c.execute('''insert into `LastView` values\
                    (%s)'''%(buff))
    conn.commit()

    # Creating two new tables called Comp_nameInfo and Comp_nameLocation for
    # each and every company in the domain.
    
    c.execute('''show tables''')
    data_comp = c.fetchall()
    chk_flag = True
    for i in range(len(data_comp)):
        if company == data_comp[i][0]:
            chk_flag = False
            break
        else:
            pass
    if chk_flag == True:

        info_tab = "`"+company+"Info"+"`"
        loc_tab = "`"+company+"Location"+"`"

        c.execute('''create table if not exists %s(`Company Name` varchar(85)\
    , Country varchar(50),`email/url` varchar(90))'''%(info_tab))
        conn.commit()

        c.execute('''create table if not exists%s(`Country` varchar(65),`City` varchar(65)\
    , Address varchar(200),`Contact Person` varchar(70),email varchar(100))'''\
                   %(loc_tab))
        conn.commit()
        

    # Creating the main table for the company which will store employee info
    
        c.execute('''create table if not exists %s(`Employee ID` varchar(100))'''\
                %(company_table_merged))
        conn.commit()
        #print "column created"
    
        for i in range(len(table_contents)):
            #print table_contents[i]
            c.execute('''alter table %s add column %s varchar(100)'''\
                      %(company_table_merged,str(table_contents[i])))
            conn.commit()

        conn.commit()

        
        c.execute('''alter table %s add column `Remarks` varchar(200)'''\
                          %(company_table_merged))
        conn.commit()

        # Now transfer the data from excel sheet into database
    
        #print count_rows
        #print rows
        #print table_contents
        #i = 0
        try:       
            for i in range(count_rows + 1,rows):
                norm_row_list = []
                row_list = sh.row_values(i)
                for z in range(len(row_list)):
                    #print row_list[z]
                    if isinstance(row_list[z],float) == True:
                        temp = str(row_list[z])
                    elif isinstance(row_list[z],int) == True:
                        temp = str(row_list[z])
                    else:
                        temp = (row_list[z])
                    #print temp
                    row_list[z] = temp
                #print row_list
                for j in index_of_valid_col:
                    norm_row_list.append(row_list[j])
                #print norm_row_list
                #print "Current row is: "+str(i)
                #for k in range(len(norm_row_list)):
                #print (table_contents[k])
                #print k
                #print norm_row_list[k]
                length = len(norm_row_list)
                string = "\""
                count = 0
            
                for m in norm_row_list:
                    if count == 0:
                        sq = string + m
                        sq = sq + "\""+","
                        count = count + 1
                    else:
                        if (count != length - 1):
                            #print m
                            sq = sq +"\""+ m
                            sq = sq + "\""+","
                            count += 1
                        else:
                            sq = sq +"\""+ m
                            sq = sq + "\""
                        #print isinstance(norm_row_list[k],list)
                buff = "\""+u"none"+"\""
                sq = "\""+str(i)+"\""+","+sq + ","+buff
                c.execute('''insert into %s values(%s)'''\
                                        %(company_table_merged,sq))
                
    
                count = 0
                sq = None
            conn.commit()
            return 1

        except:
            d = wx.MessageDialog(None,"Error on row number:%s "%(i),\
                             "Message",wx.OK)
            d.ShowModal()
            c.execute('''drop table %s'''%(company_table_merged))
            #conn.commit()
            c.execute('''drop table %s'''%(loc_tab))
            #conn.commit()
            c.execute('''drop table %s'''%(info_tab))
            conn.commit()

    else:
        d = wx.MessageDialog(None,"Company name already exists: ",\
                             "Warning",wx.OK)
        d.ShowModal()
        return 0

    
        
        

   


    
    
    
    
            
        
    
    
    
