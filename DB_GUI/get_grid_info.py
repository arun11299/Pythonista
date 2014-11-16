# This module will pass information needed to build the grid.i.e "tables present
# in the database and number of tables in the database. Also , it returns
# all the databases present in ther sql except the ones which were created
# by default by the sql. This module is imported by "show_database.py"

def main(conn,c,name):
    if name == "show_database":
        count = 0
        c.execute('''show databases''')
        data_all = c.fetchall()
        data = []
        for i in range(len(data_all)):
            if (data_all[i][0] != "information_schema")\
               and (data_all[i][0] != "test") and (data_all[i][0] != "mysql"):

                data.append((data_all[i][0]))
                count += 1

            else:
                pass
        data = tuple(data)
        print data
        row = range(count)
        return(data,row)

def tables(conn,c,domain_name):
    domain_name = "`"+domain_name+"`"
    c.execute('''use %s'''%(domain_name))
    c.execute('''show tables''')
    data = c.fetchall()
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
    
    print data_new
    return (data_new,len(data_new))    
    
