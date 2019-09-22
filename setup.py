#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------

from __future__ import absolute_import
from os import path
from setuptools import setup
from sys import version_info


# Define a read function for using README for long_description
def read(fname, fkwargs=dict()):
    return open(path.join(path.dirname(__file__), fname), **fkwargs).read()


# Define default kwargs for python2/3
read_kwargs = dict()
if version_info.major == 3:
    read_kwargs = {"encoding": "utf8"}

# Run setup
setup()
