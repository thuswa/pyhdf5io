#!/usr/bin/env python
# $Id: setup.py 30 2008-08-13 18:59:00Z thuswa $
# Last modified Sun Aug 17 16:05:10 2008 on violator
# update count: 4

from hdf5io import *



def hdf5test():
    # Create some test variables
    var = 1
    varstring='test string'
    vararray=[1, 32, 3]

    # Save to file
    hdf5save("test.h5")

    # 
    hdf5info("test.h5")





    
