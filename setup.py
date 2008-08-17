#!/usr/bin/env python
# $Id$
# Last modified Sun Aug 17 17:05:21 2008 on violator
# update count: 12

from distutils.core import setup

setup(name='pyhdf5io',
      version='0.1',
      description='Python module containing hdf5 load and save function.',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      url='http://code.google.com/p/pyhdf5io/',
      packages=['hdf5io'],
      package_data={'hdf5io': ['README','INSTALL'] },
      requires=['tables(>=2.0.4)']
      )
