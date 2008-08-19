#!/usr/bin/env python
# $Id$
# Last modified Wed Aug 20 00:02:32 2008 on violator
# update count: 301
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

Created Albert Thuswaldner 2008-07-04
"""

import tables
import inspect

###############################################################################

def hdf5info(filename):
    """
    Displays the contents of a hdf5 file.

    /Input variables
    filename: string 
    name of hdf5 file
    """
    # Open file for reading
    f=tables.openFile(filename,'r')

    # Walk through groups and display the nodes
    for group in f.walkGroups():
      for node in f.listNodes(group):
          print node

    # Close file
    f.close()

###############################################################################

def hdf5load(filename, selectvars=None, groupname="/"):
    """
    Loads variables from hdf5 file

    /Input variables
    filename: string 
    name of hdf5 file

    selectvars: string
    blank separated list of variables names to be loaded

    groupname: string
    variable group to be loaded
    """
    # Get dictonary from caller namespace
    dictvar=__magicLocals()

    # Check selectvars input 
    varnames=[]
    if type(selectvars) is str:
        varnames = selectvars.split()
    elif selectvars is not None:
        raise ValueError, "varstring must be a string!"

    # Open file for reading
    f=tables.openFile(filename,'r')

    # Walk through group and create variables in workspace
    for group in f.walkGroups(groupname):
      for node in f.listNodes(group):
          if selectvars is None or node.name in varnames: 
              dictvar[node.name] = node.read()

    # Close file
    f.close()

###############################################################################

def hdf5save(filename, varstring=None, groupname="/",mode='w'):
    """
    Saves variables to a hdf5 file

    /Input variables
    filename: string 
    name of hdf5 file

    varstring: string
    blank separated list of variables names to be saved

    groupname: string
    variable group to save to

    mode: string
    file mode (w=write, a=append)
    """
    # Get dictonary from caller namespace
    dictvar=__magicLocals()

    # Check varstring input 
    if type(varstring) is str:
        varnames = varstring.split()
    else:
        if varstring is None:
           varnames = __extractvars(dictvar)
#           print varnames   # for debugging
        else:
           raise ValueError, "varstring must be a string!"
      
    # Open file for writing
    f=tables.openFile(filename,mode)

    for key,value in dictvar.iteritems():
        for varname in varnames:
#            print key, varname  # for debugging
            if key == varname:
               f.createArray(groupname,key,value)

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


def __extractvars(vardict):
    """extract the user defined variables from global dictionary"""
    varnames=[]
    blacklist=['help','In','Out']
    for key,value in vardict.iteritems():
        if key[0] != "_" and not inspect.isclass(value) and not inspect.ismodule(value) and not inspect.isfunction(value) and key not in blacklist:
            varnames.append(key)
    return varnames

