#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
""" Tests the OMNIvals class and functions
"""

from __future__ import (print_function)
from solar_index import OMNIvals
from nose.tools import assert_raises, raises
import nose.tools
import numpy as np


class TestOMNI():

    def setup(self):
        """Runs before every method to create a clean testing setup."""
        self.testOMNI = OMNIvals()

    def teardown(self):
        """Runs after every method to clean up previous testing."""
        del self.testOMNI

    @raises(Exception)
    def test_omni_load_w_bad_directory(self):
        """Tests for non-existent directory"""
        testOMNI = OMNIvals(file_dir='bad_data')

    @raises(Exception)
    def test_omni_load_w_bad_file_name(self):
        """Tests for non-existent file"""
        testOMNI = OMNIvals(file_name='bad_data.txt')
