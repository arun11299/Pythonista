# Authentication module will pass the user name,passwd,host and database name
# to this module.This module will connect to the database using the
# python API.
import sets
import MySQLdb

def login(user_name,password,host_name):
    count = 0
    print "Starting MySQL Client Program....."
    flag = True
    while (count <= 1):
        count += 1 
        print "Trying To Connect......"

        try:
            conn = MySQLdb.connect(user = user_name,passwd = password,\
                                       host = host_name,use_unicode = True)
                                   
            flag = False
            #print flag
        except:
            #print "Access Denied"
            flag == True
            count += 1
    if flag == False:
        #print "You Have Been Authenticated!!"
        c = conn.cursor()
        return 1,conn,c
    else:
        return 0,None,None
