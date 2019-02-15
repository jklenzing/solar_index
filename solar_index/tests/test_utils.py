#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
""" Tests the utils functions
"""

from __future__ import (print_function)
from solar_index import utils
from nose.tools import assert_raises, raises
import nose.tools
import numpy as np


def test_replace_fill_array():
    """Test the replace_fill function for arrays"""
    test_vals = [-1.0, 0.0, 3.0]
    filled_vals = utils.replace_fill_array(test_vals, fill_value=-1.0)

    assert ((np.all(test_vals[1:] == filled_vals[1:])) &
            np.isnan(filled_vals[0]))


def test_replace_fill_array_numpy():
    """Test the replace_fill function for arrays with numpy data"""
    test_vals = np.array([-1.0, 0.0, 3.0])
    filled_vals = utils.replace_fill_array(test_vals, fill_value=-1.0)

    assert ((np.all(test_vals[1:] == filled_vals[1:])) &
            np.isnan(filled_vals[0]))


def test_replace_fill_single():
    """Test the replace_fill function for arrays"""
    test_val1 = -1.0
    test_val2 = 2.0
    filled_val1 = utils.replace_fill_single(test_val1, fill_value=-1.0)
    filled_val2 = utils.replace_fill_single(test_val2, fill_value=-1.0)

    assert (np.isnan(filled_val1) &
            (test_val2 == filled_val2))
