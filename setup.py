#!/usr/bin/env python
# $Id: setup.py 30 2008-08-13 18:59:00Z thuswa $
# Last modified Sun Aug 17 15:20:50 2008 on violator
# update count: 7

from distutils.core import setup

setup(name='hdf5io',
      version='0.1',
      description='Modules for ',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      url='',
      packages=['hdf5io'],
      package_dir={'potato.shock': 'potato/shock'},
      package_data={'potato.shock': ['README','INSTALL'] },
      requires=['scipy(>=0.6.0)',"numpy(>=1.1.0)"]
      )


