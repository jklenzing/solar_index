#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
"""
solar_index
-----------
Solar index information, currently focused on TIMED/SEE EUV spectra

Classes
---------------------------------------------------------------------------
SolarIndex    Solar Index data
"""
from os import path

__version__ = str('0.1a2')

_ROOT = path.abspath(path.dirname(__file__))
_data_dir = path.join(_ROOT, "data")

try:
    from solar_index import (spectral_data, omni_data, utilities)
    from solar_index.spectral_data import EUVspectra
    from solar_index.omni_data import OMNIvals
except ImportError as err:
    raise ImportError('problem importing solar_index: ' + str(err))
