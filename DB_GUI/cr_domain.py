# This module will create the database if not exists

def create_database(c,conn,domain):
    c.execute('''create database if not exists %s'''%(domain))
    conn.commit()
    c.execute('''use %s'''%(domain))
    c.execute('''show tables''')
    conn.commit()
    all_tables = c.fetchall()
    chk_flag_x = True
    for i in range(len(all_tables)):
        if all_tables[i][0] == "LastView":
            chk_flag_x = False
            break
        else:
            pass
    if chk_flag_x == True:
        c.execute('''create table `LastView`(`Company Name`\
                        varchar(65),`last view` varchar(65),Flag varchar(200))''')
        conn.commit()
        
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
        
    #print "Database Created"
    conn.commit()    
