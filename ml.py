import sys

# Print an ASCII character
def putc(obj,args):
    a0,nil,nil,nil = args
    sys.stdout.write(chr(a0))

# Print a digit
def putd(obj,args):
    a0,nil,nil,nil = args
    sys.stdout.write(str(a0))

# Print a null-terminated string
def puts(obj,args):
    pass

# Read a string from stdin
def gets(obj,args):
    pass

# Load a file
def fread(obj,args):
    pass

# Write to a file
def fwrite(obj,args):
    pass

# Get the time
def time(obj,args):
    a0,a1,nil,nil = args
    

# Quit Python
def exit(obj,args):
    a0,nil,nil,nil = args
    sys.exit(a0)
