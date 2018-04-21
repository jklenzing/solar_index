#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------
""" Common functions used for different data types and classes

Modules
-------------------------------------------------------------------------------
replace_fill_array : Replaces missing values in an array with a new value
replace_fill_single : Test value to see if it is good, and replaces if needed
-------------------------------------------------------------------------------

Moduleauthor
-------------------------------------------------------------------------------
Angeline G. Burrell, 19 April 2018, University of Texas at Dallas (UTD)
-------------------------------------------------------------------------------
"""
import logbook
import numpy as np

def replace_fill_array(data, fill_value=999.9, replace_value=np.nan):
    """ Replaces missing values in an array with a specified replacement value

    Parameters
    ----------
    data : (array like)
        Array of values with some values possibly filled by a constant
    fill_value : (float)
        Value used to denote a lack of data (default=999.9)
    replace_value : (float)
        New fill value (default=np.nan)

    Returns
    -------
    data : (np.ndarray)
        Array of values with old fill values replaced with new fill values
    """
    # Allow for array-like input
    if not isinstance(data, np.ndarray):
        try:
            data = np.array(data)
        except:
            logbook.error("input data must be a numpy array")
            return data

    data[data==fill_value] = replace_value

    return data


def replace_fill_single(data_value, fill_value=999.9, replace_value=np.nan):
    """ Tests to see if provided value is a fill value, and replaces if needed

    Parameters
    ----------
    data_value : (int/float/str/bool/NoneType)
        Array of values with some values possibly filled by a constant
    fill_value : (int/float/str/bool/NoneType)
        Value used to denote a lack of data (default=999.9)
    replace_value : (int/float/str/bool/NoneType)
        New fill value (default=np.nan)

    Returns
    -------
    new_value : (int/float/str/bool/NoneType)
        Array of values with old fill values replaced with new fill values
    """
    new_value = replace_value if data_value == fill_value else data_value

    return new_value

