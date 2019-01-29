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

    def test(self):
        assert (True)


if __name__ == '__main__':
    unittest.main()
