#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2018, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------
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
import logging

class OMNIvals:
    """ Object containing OMNI solar indices

    Parameters
    ----------


    Attributes
    ----------

    """
    def __init__(self, file_dir="data", file_name="omni2_daily_12664.txt"):

        try:
            self.load_omni_vals(file_dir,file_name)
        except:
            logging.error("unable to initiate OMNIvals class")

    def load_omni_vals(self, file_dir="data",
                         file_name="omni2_daily_12664.txt"):
        """ Load an ascii file into the OMNIvals class

        Parameters
        -----------
        file_dir : (str)
            Directory with data files (default='data')
        file_name : (str)
            Data filename (default='omni2_daily_12664.txt')

        Returns
        -------
        Void
        """

        from os import path

        # Construct filename and load the data
        assert path.isdir(file_dir), logging.error("unknown file directory")
        self.filename = ('%s/%s' % (file_dir, file_name))

        assert path.isfile(self.filename), logging.error("unknown file")

        try:
            data = np.loadtxt(self.filename)
        except:
            logging.error("unable to load ascii file")

        self.year = data[:,0]
        self.day = data[:,1]
        self.dt = np.array([dt.datetime(int(self.year[i]),1,1) +
                            dt.timedelta(days=int(self.day[i])-1)
                            for i in range(len(self.day))])

        self.Rz     = data[:,3]
        self.F107   = self._fill_nan(data[:,4])
        self.Lalpha = data[:,5]

    def _fill_nan(self, x, fill_value=999.9, replace_value=np.nan):
        """ Replaces missing values (-1) with nan

        Parameters
        ----------
        x : (np.ndarray)
            Array of values with some values possibly filled by a constant
            fill_value : (float)
                Value used to denote a lack of data (default=999.9)
            replace_value : (float)
                New fill value (default=np.nan)

        Returns
        -------
        x : (np.ndarray)
                Array of values with old fill values replaced with new fill values
        """

        assert isinstance(x, np.ndarray), \
                    logging.error("x must be a numpy array")

        x[x==fill_value] = replace_value

        return x
