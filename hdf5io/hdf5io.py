#!/usr/bin/env python
# $Id$
# Last modified Tue Jan 27 22:52:06 2009 on violator
# update count: 393
#
# pyhdf5io - Python module containing hdf5 load and save functions.
# Copyright (C) 2008  Albert Thuswaldner
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
A set of I/O functions for the hdf5 file format.

Based on pyTables to be able to save and load data to/from hdf5 files.
"""

import tables
import inspect

###############################################################################

def hdf5ls(filename):
    """
    Displays the contents of a hdf5 file.

    Syntax:
     hdf5ls('filename')
    """
    # Try to open and read from file 
    try:
        f=tables.openFile(filename,'r')

        try:
            for group in f.walkGroups():
                for node in f.listNodes(group):
                    print node
        finally:
          f.close()
    except IOError:
        print 'Cannot read:', filename

###############################################################################

def hdf5load(*args):
    """
    Loads variables from hdf5 file.
    
    Syntax:
     hdf5load('filename')
     hdf5load('filename', '/group')
     hdf5load('filename', 'var1', 'var2', ....)
     hdf5load('filename', '/group', 'var1', 'var2', ....)
     hdf5load('filename', '/group var1 var2 ....')
     hdf5load('filename', '/group var1', 'var2', 'var3 ....')

    Description: 
     hdf5load loads variables from a hdf5 file to the namespace that the
     function is called from. The syntax is flexible which means that the
     function can be called in several different ways (see above). If only
     the file name is given, all variables are loaded. In addition, if
     a group name is supplied, all variables from that group is loaded.
     It is also possible to specify exactly which variables that should
     be loaded. 
    """

    # Get dictonary from caller namespace
    dictvar=__magicLocals()

    # Extract input arguments
    inputargs=__extractargs(*args)
    filename=inputargs[0]
    groupname=inputargs[1]
    varnames=inputargs[2]

    # Try to open and read from file 
    try:
        f=tables.openFile(filename,'r')
        try:
            # Walk through group and create variables in workspace
            for group in f.walkGroups(groupname):
                # Walk through only the leaves (don't list the groups)
                for leaf in group._f_walkNodes('Leaf'):
                    if not varnames or leaf.name in varnames: 
                        dictvar[leaf.name] = leaf.read()
        finally:
           f.close()
    except IOError:
        print 'Cannot read:', filename

###############################################################################

def hdf5save(*args):
    """
    Saves variables to a hdf5 file.
    
    Syntax:
     hdf5save('filename')
     hdf5save('filename', '/group')
     hdf5save('filename', 'var1', 'var2', ....)
     hdf5save('filename', '/group', 'var1', 'var2', ....)
     hdf5save('filename', '/group var1 var2 ....')
     hdf5save('filename', '/group var1', 'var2', 'var3 ....')

    Description: 
     hdf5save saves variables from the current namespace to a hdf5 file.
     The syntax is flexible which means that the function can be called
     in several different ways (see above). If only the file name is given,
     all variables are saved to the root group of the hdf5 file. In addition,
     if a group name is supplied, all variables can be saved to a specific
     group. It is also possible to specify exactly which variables that should
     be saved. 
    """
    mode='w'
    
    # Get dictonary from caller namespace
    dictvar=__magicLocals()

    # Extract input arguments
    inputargs=__extractargs(*args)
    filename=inputargs[0]
    groupname=inputargs[1]
    varnames=inputargs[2]

    # If no variables specified by the user 
    if not varnames:
        varnames = __extractvars(dictvar)
        # print varnames   # for debugging

    # Open file for writing
    f=tables.openFile(filename,mode)

    # Create group
    g=f.root  
    if groupname != "/":
        grouplist = groupname.split('/')
        for group in grouplist:
            if group:
                g=f.createGroup(g,group)

    for key,value in dictvar.iteritems():
        for varname in varnames:
#            print key, varname  # for debugging
            if key == varname:
               f.createArray(g,key,value)

    # Close file
    f.close()

###############################################################################
# Helper functions

# Not used
def __magicGlobals(level=1):
    r"""Return the globals of the *caller*'s caller (default), or `level`
    callers up."""
    return inspect.getouterframes(inspect.currentframe())[1+level][0].f_globals

# used
def __magicLocals(level=1):
    r"""Return the locals of the *caller*'s caller (default) , or `level`
    callers up.
    """
    return inspect.getouterframes(inspect.currentframe())[1+level][0].f_locals

def __extractargs(*args):
    """check and identify input variables"""  
    if len(args) >= 1:
        # transform args tuple to list
        arglist=list(args)
        # Pop the presumed filename from the args list 
        filename=arglist.pop(0)
        # loop the rest of the args list and extract group/variable names
        varnames=[]
        for arg in arglist:
            if type(arg) is str:
                varnames = varnames+arg.split()
            else:
                raise ValueError, "variable input must be of type string"
    else:
        raise ValueError, "Too few arguments"

    # Check if varname list contains a group name
    groupname="/"
    if varnames:
        if varnames[0][0] == "/":
            groupname=varnames.pop(0)

    return (filename, groupname, varnames)
        
def __extractvars(vardict):
    """extract the user created variables from global dictionary"""
    varnames=[]
    blacklist=['help','In','Out']
    for key,value in vardict.iteritems():
        if key[0] != "_" \
               and not inspect.isclass(value) \
               and not inspect.ismodule(value) \
               and not inspect.isfunction(value) \
               and key not in blacklist:
            varnames.append(key)
    return varnames

