#!/usr/bin/env python
# $Id$
# Last modified Sun Aug 17 17:05:49 2008 on violator
# update count: 5

from hdf5io import *

# test function
def hdf5test():
    # Create some test variables
    var = 1
    varstring='test string'
    vararray=[1, 32, 3]

    # Save to file
    hdf5save("test.h5")

    # 
    hdf5info("test.h5")





    
