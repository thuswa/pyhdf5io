#!/usr/bin/env python
# $Id$
# Last modified Mon Aug 18 08:40:25 2008 on CO-W02454 by thuswa
# update count: 24

from distutils.core import setup

setup(name='pyhdf5io',
      version='0.1',
      description='Python module containing hdf5 load and save functions.',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      license='GPLv3',
      url='http://pyhdf5io.googlecode.com',
      packages=['hdf5io'],
      package_dir = {'hdf5io' : 'src' },
      requires=['tables(>=2.0.0)']
      )
