#!/usr/bin/env python
# $Id$
# Last modified Mon Aug 18 22:02:41 2008 on violator
# update count: 9

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
    hdf5info("test.h5")

    # Append a variable
    var2=67.3
    hdf5save("test.h5",'var2',"/",'a')

    # Show file content again 
    hdf5info("test.h5")

    
