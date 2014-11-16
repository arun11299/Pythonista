# This module takes the list of column name and merges it so that
# it is compatible with MySQL syntax.

def split_merge(first_row_val):
    merged_first_row_val = []

    if isinstance(first_row_val,list):
        length = len(first_row_val)
        print "length is: "+str(length)
        for i in range(length):
            string = first_row_val[i]
            string = string.split()
            length = len(string)
            if length == 1:
                string = string[0]+''
                merged_first_row_val.append(string)
            else:
                for i in range(length-1):
                    string = string[0]+string[i+1]
                    merged_first_row_val.append(string)

        return(merged_first_row_val)

    else:
        string = first_row_val
        string = string.split()
        length = len(string)
        if length == 1:
                string = string[0]+''
                merged_first_row_val = string
        else:
            for i in range(length-1):
                string = string[0]+string[i+1]

        merged_first_row_val = string
        return(merged_first_row_val)
        

        
