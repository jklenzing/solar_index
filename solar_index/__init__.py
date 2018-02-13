#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------
"""
solar_index
-----------
Solar index information, currently focused on TIMED/SEE EUV spectra

Classes
---------------------------------------------------------------------------
SolarIndex    Solar Index data
"""
import logging

__version__ = str('0.1a1')

# Imports
#---------------------------------------------------------------------

try:
    import solar_index
    from solar_index import (SolarIndex)
except ImportError as e:
    logging.exception('problem importing solar_index: ' + str(e))
