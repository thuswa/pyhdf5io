#!/usr/bin/env python
# Last modified Thu May  9 22:29:02 2013 on havoc
# update count: 37

from distutils.core import setup

from hdf5io import __version__

setup(name='pyhdf5io',
      version=__version__,
      description='Python module containing high-level hdf5 load and save functions.',
      author='Albert Thuswaldner',
      author_email='thuswa@gmail.com',
      license='GPL',
      long_description = """
      People familiar with Matlab(TM) and its load and save functions will find 
      themselves at home with this small python module, I guess. It makes it 
      possible to save your variables in "workspace" or from within a function 
      to a hdf5 file, and later load them back in again.
      """,
      url='http://pyhdf5io.googlecode.com',
      packages=['hdf5io'],
      package_dir = {'hdf5io' : 'hdf5io' },
      platforms='any',
      requires=['tables(>=2.0.0)']
      )
