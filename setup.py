#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------

from __future__ import absolute_import
from os import path
from setuptools import setup, find_packages
from sys import version_info

# Define a read function for using README for long_description

def read(fname, fkwargs=dict()):
    return open(path.join(path.dirname(__file__), fname), **fkwargs).read()

# Define default kwargs for python2/3
read_kwargs = dict()
if version_info.major == 3:
    read_kwargs = {"encoding":"utf8"}

# Run setup

setup(name='solar_index',
      version='0.1a2',
      url='github.com/jklenzing/solar_index',
      author='Jeff Klenzing',
      author_email='jeffrey.klenzing@nasa.gov',
      description='Prepares solar irradiance index based on TIMED/SEE data',
      long_description=read('README.md', read_kwargs),
      packages=find_packages(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Scientific/Engineering :: Physics",
          "Intended Audience :: Science/Research",
          "License :: BSD",
          "Natural Language :: English",
          "Programming Language :: Python :: 2.7",
          "Programming Language :: Python :: 3.4",
          "Programming Language :: Python :: 3.5",
          "Programming Language :: Python :: 3.6",
          "Operating System :: MacOS :: MacOS X",
          "Operating System :: POSIX",
      ],
      install_requires=[
          'numpy',
          'logbook'
      ],
      include_package_data=True,
      zip_safe=False,
)
