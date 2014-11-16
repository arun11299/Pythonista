''' Program to import excel sheet database into MySQL database'''
# This is the main file

import sets
import MySQLdb  # MySQL API for Python
import ch_dir   # Module for changing directory
#import xlrd     # Module for reading .xls file in Python
import commands # Module for executing command
import os
import domain_create # This module creates the database
import transfer_data # This module reads from the excel sheet
import merge         # Module for removing space in between names 

count = 0
print "Starting MySQL Client Program....."
flag = True
while (flag == True):
    if (count <= 1):
        count += 1 
        password = raw_input("Enter Password For Root User: ")
    
        print "Trying To Connect......"

        try:
            conn = MySQLdb.connect(user = "root",passwd = password,host = \
                                   "localhost")
            flag = False
            print flag
        except:
            print "Access Denied"
            flag == True

    else:
        print "Closing The Application"
        exit()

print "You Have Been Authenticated!!"
c = conn.cursor()

# Open the directory containing the file

print "NOTE:DOmain name should be written without giving space"
domain = raw_input("Enter The Domain Of The Company: ")
ch_dir.cd()
fh = os.popen("ls -l") # Needs To be changed acc. to OS
struct_list = fh.readlines()

print "Files/Folders Present In This Directory"
for i in struct_list:
    print i

# Go into the company's folder containing the excel sheets
company_table = raw_input("Enter The Name Of The Company: ")
company_table_merged = merge.split_merge(company_table)
company = raw_input("Enter the name of the file(without extention): ")
ch_dir.cd()
fh = os.popen("ls -l")
struct_list = fh.readlines()

print "Files Present In This Directory"
for i in struct_list:
    print i

# Create Database
domain_create.create_database(c,conn,domain)

#Start Reading From The Excel Sheet

transfer_data.transfer(c,conn,company,company_table_merged,domain)
print "Database Transfered to MySQl :-)"






