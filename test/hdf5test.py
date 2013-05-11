#!/usr/bin/env python
# Last modified Sat May 11 13:19:48 2013 on havoc
# update count: 47

from hdf5io import *
from numpy import array 

# - Test supported types
varint = 1
varfloat = 3.14159
#varstring='test string'
varcomplex=(1-4j)
ivarlist=[1, 32, 3]
#vartuple = (1, 2, 'test string')
vararray = array([1,2,3])
#vararrays = array([(1,2,3,'a'), (2,3,5,'b')])
vararrayc = array( [ [1,2], [3,4] ], dtype=complex )

# Save to file
hdf5save("test.h5")

# Show file content 
hdf5ls("test.h5")

# - Append a variable
var2=67.3
hdf5save("+test.h5",'var2',"/")

# Show file content again 
hdf5ls("test.h5")

# - Add group
var2=67.3
hdf5save("+test.h5",'var2',"/test")

# Show file content again 
hdf5ls("test.h5")
 
