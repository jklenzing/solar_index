#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
"""
solar_index
-----------
Solar index information, currently focused on TIMED/SEE EUV spectra

"""

from os import path

__version__ = str('0.2-alpha')

_ROOT = path.abspath(path.dirname(__file__))
_data_dir = path.join(_ROOT, "data")

try:
    from solar_index._core_class import SolarIndex  # noqa: F401
    from solar_index._spectral_data import EUVspectra  # noqa: F401
    from solar_index._omni_data import OMNIvals  # noqa: F401
except ImportError as err:
    raise ImportError('problem importing solar_index: ' + str(err))
