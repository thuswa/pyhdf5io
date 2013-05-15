#!/usr/bin/env python3
# encoding: utf-8
# Last modified Wed May 15 08:13:26 2013 on havoc
# update count: 96

from hdf5io import *
from numpy import array 

def testsavetypes():
    """ Test saveing supported variable types """
    varint = 1
    varfloat = 3.14159
    varstring="test string"
    varcomplex=(1-4j)
    varlist=[1, 32, 3]
    varlists=[1, 32, 'test string']
    vartuple = (1, 2, 3)
    vartuples = (1, 2, 'test string')
    vararray = array([1,2,3])
    #vararrays = array([(1,2,3,'a'), (2,3,5,'b')])
    vararrayc = array( [ [1,2], [3,4] ], dtype=complex )

    # Save to file
    hdf5save("test.h5")
    return locals()

def showfile():
    """" Show file content """ 
    hdf5ls("test.h5")

def testappend(): 
    """ Test to append variable """
    var2=67.3
    hdf5save("+test.h5",'var2',"/")

def testaddgroup():
    """ Test to add a group """
    var2=67.3
    var3="group test"
    hdf5save("+test.h5",'var2',"/test")

def testloadtypes():
    """ Test loading supported variable types """
    hdf5load("test.h5")
    return locals()

def testloadgroup():
    """ Test loading supported variable types """
    
def hdf5test():
    """ Main test function """
    savedict = testsavetypes()
    showfile()
    #print(savedict)
    loaddict = testloadtypes()
    #print(loaddict)
    if savedict == loaddict:
        print("load/save success!")
    else:
        print("load/save FAILURE!")
    testappend()
    showfile()
    testaddgroup()
    showfile()

if __name__ == '__main__':
    hdf5test()
