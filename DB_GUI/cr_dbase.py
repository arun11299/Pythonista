''' Program to import excel sheet database into MySQL database'''
# This is the main file


def create_database(conn,c,domain,company,file_name,dir_name,major_name):
    import sets
    import MySQLdb  # MySQL API for Python
    import chg_dir   # Module for changing directory
    #import xlrd     # Module for reading .xls file in Python
    import commands # Module for executing command
    import os
    import cr_domain # This module creates the database
    import transfer_database # This module reads from the excel sheet
    import merge         # Module for removing space in between names 

# Open the directory containing the file

    #print "NOTE:DOmain name should be written without giving space"
    #domain = raw_input("Enter The Domain Of The Company: ")
    chg_dir.cd(dir_name)
    #fh = os.popen("ls -l") # Needs To be changed acc. to OS
    #struct_list = fh.readlines()

    #print "Files/Folders Present In This Directory"
    #for i in struct_list:
    #    print i

# Go into the company's folder containing the excel sheets
    #company_table = raw_input("Enter The Name Of The Company: ")
    #company_table_merged = merge.split_merge(company_table)
    company_table_merged = "`"+company+"`"
    #company = raw_input("Enter the name of the file(without extention): ")
    #ch_dir.cd()
    #fh = os.popen("ls -l")
    #struct_list = fh.readlines()

    #print "Files Present In This Directory"
    #for i in struct_list:
        #print i

# Create Database
    domain = "`"+domain+"`"
    cr_domain.create_database(c,conn,domain)

#Start Reading From The Excel Sheet

    ret_val = transfer_database.transfer(c,conn,file_name,company_table_merged,domain,\
                               company,major_name)
    #print "Database Transfered to MySQl :-)"
    return (ret_val)





