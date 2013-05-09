#!/usr/bin/env python
# Last modified Thu May  9 22:28:50 2013 on havoc
# update count: 12

from hdf5io import *

# test function
def hdf5test():
    # Create some test variables
    var = 1
    varstring='test string'
    vararray=[1, 32, 3]

    # Save to file
    hdf5save("test.h5")

    # Show file content 
    hdf5ls("test.h5")

    # Append a variable
    var2=67.3
    hdf5save("test.h5",'var2',"/",'a')

    # Show file content again 
    hdf5ls("test.h5")

    
