# This module creates any new table in a database.This module is imported from
# module "show_table_col.py".This implements one of the functions required in
# that module which in turn is acalled by module "show_database.py".

# This module saves the data entered into the grid into the sql database.

## NOTE:
# When we are updating a table we first drop that table and load the table
# into the database again. So, during that time we need not create the "info"
# and "location" table again.

def col_headers(conn,c,domain_name,comp_name_esc,col_header,comp_name,major_name):
    flag = True
    domain_name = "`"+domain_name+"`"
    c.execute('''use %s'''%(domain_name))
    len_col_headers = range(len(col_header))
    c.execute('''show tables''')
    tab_data = c.fetchall()
    try:
        # Check if major name already exists in the table
        # if exists do not enter it again
        if major_name != None:
            c.execute('''select * from `MajorName`''')
            table_contents = c.fetchall()
            buf_flag = True
            for i in range(len(table_contents)):
                if table_contents[i][0] == major_name:
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
            
        ##
        
        info_tab = "`"+comp_name+"Info"+"`"
        c.execute('''create table if not exists %s(`Company Name` varchar(85)\
            , Country varchar(50),`email/url` varchar(90))'''%(info_tab))
        conn.commit()
        loc_tab = "`"+comp_name+"Location"+"`"
        print loc_tab
        c.execute('''create table if not exists %s(`Country` varchar(65),`City` varchar(65)\
, Address varchar(200),`Contact Person` varchar(70),email varchar(100))'''%(loc_tab))
        print "created"
        conn.commit()
        c.execute('''create table %s(%s varchar(150))'''\
                  %(comp_name_esc,str(col_header[0])))
        conn.commit()
        for i in len_col_headers[1:]:
            c.execute('''alter table %s add column %s varchar(150)'''\
                         %(comp_name_esc,str(col_header[i])))
        conn.commit()
        print "table created!!!"
    except:
        flag = False

    if flag == True:
        return(1)
    else:
        return(0)

def enter_data(conn,c,domain_name,comp_name_esc,cell_data,comp_name):
    length = len(cell_data)
    string = "\""
    count = 0
    flag = True        
    for m in cell_data:
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
    try:
        c.execute('''insert into %s values (%s)'''%(comp_name_esc,sq))
        #conn.commit()
        sq = None
        count = 0
    except:
        flag = False


    return(flag)
