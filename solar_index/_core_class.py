#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2019, JK
# Full license can be found in License.md
# -----------------------------------------------------------------------------
"""Wrapper for running sami2 model

Classes
-------------------------------------------------------------------------------
SolarIndex    Solar Index data
-------------------------------------------------------------------------------


Moduleauthor
-------------------------------------------------------------------------------
Jeff Klenzing (JK), 10 July 2019, Goddard Space Flight Center (GSFC)
-------------------------------------------------------------------------------
"""

import pysat

start = pysat.datetime(2003, 1, 1)
stop = pysat.datetime(2003, 1, 31)


class SolarIndex(object):
    """Python object to handle solar indices
    """

    def __init__(self, start=start, stop=stop):
        """Initializes object to compare Indices

        Parameters
        ----------
        start : (pysat.datetime)
            Date of the beginning of the comparison period
        stop : (pysat.datetime)
            Date of the end of the comparison period

        Attributes
        ----------
        f107 : (pysat.instrument)
            Holds the solar F10.7 index values

        """

        self.f107 = pysat.Instrument(platform='sw', name='f107')
        self.f107.load(date=start)

    def _check_for_data(inst=None, start=start, stop=stop):
        """Checks to see if data has been downloaded in pysat
        """

    def _load_data(inst=None, start=start, stop=stop):
        """Loads data from pysat
        """
        inst.load(start, stop)

        return
