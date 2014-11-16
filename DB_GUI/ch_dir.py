# Changing Current Working directory

def cd():
    import os
    print "Your Present Working Directory Is ..."
    print os.getcwd()
    path=raw_input("Enter the path to your domain/company: ")
    os.chdir(path)
    print "Now Your Changed Working Directory Is ..."
    print os.getcwd()
