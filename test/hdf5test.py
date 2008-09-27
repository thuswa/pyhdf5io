#!/usr/bin/env python
# $Id$
# Last modified Sat Sep 27 19:14:23 2008 on violator
# update count: 10

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
    hdf5info("test.h5")

    
