#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
""" Tools for loading solar indices.

Classes
-------------------------------------------------------------------------------
OMNIvals

Moduleauthor
-------------------------------------------------------------------------------
Jeff Klenzing (JK), 3 Mar 2018, Goddard Space Flight Center (GSFC)

References
-------------------------------------------------------------------------------
"""

import datetime as dt
import numpy as np


class OMNIvals:
    """ Object containing OMNI solar indices

    Keyword Arguments
    ------------------
        file_dir : (str)
            Directory with data files (default=solar_index._data_dir)
        file_name : (str)
            Data filename (default='omni2_daily_12664.txt')

    Attributes
    ----------
    self.year : (np.array)
        Integer year
    self.day : (np.array)
        Integer day
    self.dt : (np.array)
        datetime
    self.Rz : (np.array)
        Rz index
    self.F107 : (np.array)
        10.7 cm flux index in solar flux units
    self.Lalpha : (np.array)
        Lyman alpha

    Methods
    --------
    load_omni_vals : Load the values from an ASCII file
    """
    def __init__(self, **kwargs):

        try:
            self.load_omni_vals(**kwargs)
        except:
            logging.error("unable to initiate OMNIvals class")

    def load_omni_vals(self, **kwargs):
        """ Load an ascii file into the OMNIvals class

        Keyword Arguments
        --------------------
        file_dir : (str)
            Directory with data files (default='data')
        file_name : (str)
            Data filename (default='omni2_daily_12664.txt')

        Returns
        -------
        Void
        """

        from os import path
        from solar_index import utilities, _data_dir

        # Define the default data file and update using kwargs
        file_dir = _data_dir
        file_name = "omni2_daily_12664.txt"

        for kk in kwargs.keys():
            if kk.lower() == "file_dir":
                file_dir = kwargs[kk]
            elif kk.lower() == "file_name":
                file_name = kwargs[kk]

        # Construct filename and load the data
        if not path.isdir(file_dir):
            raise FileNotFoundError("unknown file directory {:s}".format(file_dir))
        self.filename = path.join(file_dir, file_name)

        if not path.isfile(self.filename):
            raise FileNotFoundError("unknown file {:s}".format(self.filename))

        try:
            data = np.loadtxt(self.filename)
        except:
            estr = "unable to load ascii file {:s}".format(self.filename)
            raise ImportError(estr)

        self.year = data[:, 0]
        self.day = data[:, 1]
        self.dt = np.array([dt.datetime(int(self.year[i]), 1, 1) +
                            dt.timedelta(days=int(self.day[i])-1)
                            for i in range(len(self.day))])

        self.Rz = data[:, 3]
        self.F107 = utilities.replace_fill_array(data[:, 4], fill_value=999.9)
        self.Lalpha = data[:, 5]
