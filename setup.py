#!/usr/bin/env python
# $Id$
# Last modified Mon Aug 18 22:17:04 2008 on violator
# update count: 26

from distutils.core import setup

setup(name='pyhdf5io',
      version='0.2',
      description='Python module containing hdf5 load and save functions.',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      license='GPLv3',
      url='http://pyhdf5io.googlecode.com',
      packages=['hdf5io'],
      package_dir = {'hdf5io' : 'hdf5io' },
      requires=['tables(>=2.0.0)']
      )
