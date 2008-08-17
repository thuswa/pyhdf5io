#!/usr/bin/env python
# $Id$
# Last modified Sun Aug 17 20:38:45 2008 on violator
# update count: 18

from distutils.core import setup

setup(name='pyhdf5io',
      version='0.1',
      description='Python module containing hdf5 load and save function.',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      license='GPLv3',
      url='http://pyhdf5io.googlecode.com',
      packages=['hdf5io'],
      package_data = {'hdf5io' : 'src/' },
      package_data={'hdf5io': ['README','INSTALL'] },
      requires=['tables(>=2.0.0)']
      )
