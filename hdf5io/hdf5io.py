#!/usr/bin/env python
# encoding: utf-8
# Last modified Wed May 15 20:05:01 2013 on havoc
# update count: 570
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

"""
A set of I/O functions for the hdf5 file format.

Based on pyTables to be able to save and load data to/from hdf5 files.
"""
from __future__ import print_function

import inspect
import re
import tables

debug = 0 

###############################################################################

def hdf5ls(*args):
    """
    Displays the contents of a hdf5 file.

    Syntax:
     hdf5ls()
     hdf5ls('filename')

     Calling this function with no arguments assumes the default
     file name \"hdf5io.h5\"
    """
    # Check input arguments
    if len(args) == 0:
        filename = "hdf5io.h5"
    elif len(args) == 1:
        filename = args[0]
    else:
        raise ValueError("Too many arguments")        
    
    # Try to open and read from file 
    print("Listing content of:", filename)
    try:
        f=tables.openFile(filename,'r')

        try:
            for group in f.walkGroups():
                for node in f.listNodes(group):
                    print(node)
        finally:
          f.close()
    except IOError:
        print('Cannot read:', filename)

###############################################################################

def hdf5load(*args):
    """
    Loads variables from hdf5 file.
    
    Syntax:
     hdf5load()
     hdf5load('filename')
     hdf5load('filename', 'v*')
     hdf5load('filename', '/group')
     hdf5load('filename', 'var1', 'var2', ....)
     hdf5load('filename', '/group', 'var1', 'var2', ....)
     hdf5load('filename', '/group var1 var2 ....')
     hdf5load('filename', '/group var1', 'var2', 'var3 ....')

    Description:
     hdf5load loads variables from a hdf5 file to the namespace from where
     the function is called. The syntax is flexible which means that the
     function can be called in several different ways (see above). When this
     function is called with no arguments it will default to try loading all
     variables from a file called \"hdf5io.h5\". The user has also the
     option to specify a file name. In addition, if a group name is supplied,
     all variables from that group is loaded. It is also possible to specify
     exactly which variables that should be loaded either by the complete
     variable name or by using wildcards '*'.
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
                    if not varnames or varnames.match(leaf.name): 
                        if debug:
                            print(leaf.name,' : ',leaf.read())
                            print(leaf.name,' : ',__stringdecoder(leaf.read()))
                        dictvar[leaf.name] = __stringdecoder(leaf.read())
        finally:
           f.close()
    except IOError:
        print('Cannot read:', filename)

###############################################################################

def hdf5save(*args):
    """
    Saves variables to a hdf5 file.
    
    Syntax:
     hdf5save()
     hdf5save('filename')
     hdf5save('filename', 'v*')
     hdf5save('filename', '/group')
     hdf5save('filename', 'var1', 'var2', ....)
     hdf5save('filename', '/group', 'var1', 'var2', ....)
     hdf5save('filename', '/group var1 var2 ....')
     hdf5save('filename', '/group var1', 'var2', 'var3 ....')
     hdf5save('+filename')
     
    Description:
     hdf5save saves variables from the current namespace to a hdf5 file.
     The syntax is flexible which means that the function can be called
     in several different ways (see above). When this function is called with
     no arguments it will default to saving all local variables to the root
     group of a file called \"hdf5io.h5\". The user has also the option to
     specify the file name. In addition, if a group name is supplied, all
     variables can be saved to a specific group. It is also possible to
     specify exactly which variables that should be saved either by the
     complete variable name or by using wildcards '*'. Appending data
     to an existing hdf5 file is possible. To invoke this special mode
     just add a + sign to the beginning of the file name.  
    """
    # Get dictonary from caller namespace
    dictvar=__magicLocals()

    # Extract input arguments
    inputargs=__extractargs(*args)
    filename=inputargs[0]
    groupname=inputargs[1]
    varnames=inputargs[2]
    mode=inputargs[3]
    
    # Open file for writing
    f=tables.openFile(filename,mode)

    # Create group
    g=f.root  
    if groupname != "/":
        grouplist = groupname.split('/')
        for group in grouplist:
            # Check if group exists
            if g.__contains__(group): 
                g=g._f_getChild(group)
            else:
                if group:
                    g=f.createGroup(g,group)

    for key,value in dictvar.items():
        if varnames.match(key) and __checkvars(key, value):
            if debug:
                print(key,' : ',value)
                print(key,' : ',__stringencoder(value))
            f.createArray(g,key,__stringencoder(value))
    # Close file
    f.close()

###############################################################################
# Helper functions

def __magicLocals(level=1):
    """ Return the locals of the caller's caller (default),
        or or set caller level. """
    return inspect.getouterframes(inspect.currentframe())[1+level][0].f_locals

def __extractargs(*args):
    """check and identify input variables"""  

    groupname="/"
    varmatch='.'
    first=1
    mode="w"
    
    if len(args) >= 1:
        # transform args tuple to list
        arglist=list(args)
        if debug:
            print(arglist)
        # Pop the presumed filename from the args list 
        filename=arglist.pop(0)
        # Check if append (only applicable for hdf5save) 
        if filename[0] == "+":
            mode="a"
            filename=filename[1:]
            
        # loop the rest of the args list and extract group/variable names
        for arg in arglist:
            if isinstance(arg, str):
                varlist=arg.split()
                for var in varlist:
                    # Check if variable name list contains a group name
                    if var[0] == "/":
                        groupname=var
                    else:
                        if first:  
                            varmatch=var
                            first=0
                        else:
                            varmatch = varmatch+'|'+var
            else:
                raise ValueError("variable input must be of type string")
    else:
        filename = "hdf5io.h5"

    # Compile regular expression from match list
    if varmatch:
        varmatch='('+varmatch.replace("*",".*")+')'


    varnames=re.compile(varmatch)
    
    if debug:
        print(filename, groupname, varmatch, mode)
    return (filename, groupname, varnames, mode)
        
def __checkvars(key, value):
    """ Check variables against blacklist """
    blacklist=['help','In','Out']
    if key[0] == "_" \
           or inspect.isclass(value) \
           or inspect.ismodule(value) \
           or inspect.isfunction(value) \
           or inspect.ismethod(value) \
           or inspect.isbuiltin(value) \
           or key in blacklist:
        return 0
    else:
        return 1

def __stringencoder(var):
    """ pyTables can not handle unicode strings. """
    if isinstance(var, str):
        # simple string encode to binary
        return var.encode('utf-8')
    elif isinstance(var, tuple):
        # covert to list handle it as such and return tuple
        return tuple(__stringencoder(list(var)))
    elif isinstance(var, list):
        # search for string in list and encode to binary string
        return [ x.encode('utf-8') if isinstance(x, str) else x for x in var]
    else:
        return var

def __stringdecoder(var):
    """ pyTables can not handle unicode strings. """
    if isinstance(var, bytes):
        # simple string encode to binary
        return var.decode('utf-8')
    elif isinstance(var, tuple):
        # covert to list handle it as such and return tuple
        return tuple(__stringdecoder(list(var)))
    elif isinstance(var, list):
        # search for string in list and encode to binary string
        return [ x.decode('utf-8') if isinstance(x, bytes) else x for x in var]
    else:
        return var

