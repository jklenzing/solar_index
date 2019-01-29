#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
""" Tests the EUVspectra class and functions
"""

from __future__ import (print_function)
from solar_index import EUVspectra
from nose.tools import assert_raises, raises
import nose.tools
import numpy as np


class TestEUV():

    def setup(self):
        """Runs before every method to create a clean testing setup."""
        self.testEUV = EUVspectra()

    def teardown(self):
        """Runs after every method to clean up previous testing."""
        del self.testEUV

    @raises(Exception)
    def test_euv_load_w_bad_directory(self):
        """Tests for non-existent directory"""
        testEUV = EUVspectra(file_dir='bad_data')

    @raises(Exception)
    def test_euv_load_w_bad_file_name(self):
        """Tests for non-existent file"""
        testEUV = EUVspectra(file_name='bad_data.ncdf')
