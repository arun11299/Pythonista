# This module will create the database if not exists

def create_database(c,conn,domain):
    
    c.execute('''create database if not exists %s'''%(domain))
    print "Database Created"
    conn.commit()    
