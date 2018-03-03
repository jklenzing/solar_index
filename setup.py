#!/usr/bin/env python
#-*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------

from os import path
from setuptools import setup, find_packages

# Define a read function for using README for long_description

def read(fname):
    return open(path.join(path.dirname(__file__), fname)).read()

# Run setup

setup(name='solar_index',
      version='0.1a2',
      url='github.com/jklenzing/solar_index',
      author='Jeff Klenzing',
      author_email='jeffrey.klenzing@nasa.gov',
      description='Prepares solar irradiance index based on TIMED/SEE data',
      long_description=read('README.md'),
      packages=find_packages(),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Topic :: Scientific/Engineering :: Physics",
          "Intended Audience :: Science/Research",
          "License :: BSD",
          "Natural Language :: English",
          "Programming Language :: Python :: 3.6",
          "Operating System :: MacOS :: MacOS X",
      ],
      include_package_data=True,
      zip_safe=False,
)
