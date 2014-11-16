# This Module will read from the excel sheet
import xlrd
import merge
import time
def transfer(c,conn,company,company_table_merged,domain):
    count_rows = 0
    count_cols = 0
    flag = False
    try:
        work_book = xlrd.open_workbook(company+".xls")
    except IOError:
        print "File Does Not Exist"
        print "Check File Name Carefully"
    sheet = work_book.sheet_names()
    print "sheet name is: "+str(sheet[0])
    try:
        sh = work_book.sheet_by_name(sheet[0])
    except XLRDError:
        print "No Sheet Found!"
    rows = sh.nrows
    print "Number Of Rows: "+str(rows)
    cols  = sh.ncols
    print "Number Of Columns: "+str(cols)

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
    merged_first_row_val = merge.split_merge(first_row_val)
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
    #print table_contents
    ## To include special characters (&,%,$,@) in the column name
    ## warp the string inside `string`
        
    for z in range(len(table_contents)):
            temp = str(table_contents[z])
            temp = "`"+temp+"`"
            table_contents[z] = temp
            
    # Now create table
    c.execute('''use %s'''%domain)

    c.execute('''create table %s(%s varchar(100))'''\
              %(company_table_merged,str(table_contents[0])))
    conn.commit()
    print "column created"
    for i in index_of_valid_col[1:]:
        print table_contents[i]
        c.execute('''alter table %s add column %s varchar(100)'''\
                  %(company_table_merged,str(table_contents[i])))
        conn.commit()

    conn.commit()

    # Now transfer the data from excel sheet into database
    
    print count_rows
    print rows
    print table_contents
    
    for i in range(count_rows + 1,rows):
        norm_row_list = []
        row_list = sh.row_values(i)
        for z in range(len(row_list)):
            temp = str(row_list[z])
            row_list[z] = temp 
        #print row_list
        for j in index_of_valid_col:
            norm_row_list.append(row_list[j])
        print norm_row_list
        print "Current row is: "+str(i)
        #for k in range(len(norm_row_list)):
        #print (table_contents[k])
        #print k
        #print norm_row_list[k]
        length = len(norm_row_list)
        string = "\""
        count = 0
            
        for m in norm_row_list:
            if count == 0:
                sq = string + str(m)
                sq = sq + "\""+","
                count = count + 1
            else:
                if (count != length - 1):
                    print m
                    sq = sq +"\""+ str(m)
                    sq = sq + "\""+","
                    count += 1
                else:
                    sq = sq +"\""+ str(m)
                    sq = sq + "\""

            #print isinstance(norm_row_list[k],list)
        c.execute('''insert into %s values(%s)'''\
                        %(company_table_merged,sq))
        conn.commit()

        count = 0
        sq = None

    


    
    
    
    
            
        
    
    
    
