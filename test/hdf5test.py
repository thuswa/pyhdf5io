#!/usr/bin/env python3
# encoding: utf-8
# Last modified Wed May 15 08:28:21 2013 on havoc
# update count: 97
#
# pyhdf5io - Python module containing hdf5 load and save functions.
# Copyright (C) 2008-2013  Albert Thuswaldner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

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
