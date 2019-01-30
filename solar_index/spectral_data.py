#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
# -----------------------------------------------------------------------------
""" Tools for calculating integrated solar indices from EUV Spectra.

Classes
-------------------------------------------------------------------------------
EUVspectra

Moduleauthor
-------------------------------------------------------------------------------
Jeff Klenzing (JK), 22 Nov 2017, Goddard Space Flight Center (GSFC)

References
-------------------------------------------------------------------------------
Richards, P.G., 1994
Solomon et al, 2005
"""

import datetime as dt
import numpy as np


class EUVspectra(object):
    """ Object containing TIMED/SEE EUV spectra and derived indices

    Parameters
    ----------
    file : (string)
        name of data file to input (default='data/latest_see_L3_merged.ncdf')

    Returns
    -------
    self : (class SolarIndex)
        A class object containing TIMED/SEE EUV spectra and derived indices

    Attributes
    ----------
    filename : (str)
        Name of TIME/SEE data file
    year : (int)
        Year of TIMED/SEE data
    day : (int)
        day of year for TIMED/SEE data
    dt : (datetime)
        datetime object
    cor_1au : (float)
        Correction factor to 1 AU
    He2 : (float)
        HeII emission line (30.4 nm)
    species : (list)
        List of possible species
    sp_wave : (float)

    sp_flux : (float)

    line_wave : (float)

    line_flux : (float)

    oxygen : (float)
        Derived integrated avergae power delivered to Oxygen atoms
    n2 : (float)
        Derived integrated avergae power delivered to Nitrogen molecules
    o2 : (float)
        Derived integrated avergae power delivered to Oxygen molecules
    bins : (float)
        coordinates of min and max of each bin in nm
    area : (float)
        The corresponding ionization cross-section (m^2)

    Methods
    -------
    load_euv_spectra(**kwargs)
        Load the EUV spectra from a TIMED/SEE file
    integrate_power(species)
        Integrate the power for selected species
    _integrate_bin(species, iarea)
        Integrates sp_flux over bin values
    load_coeff(species)
        Generates bins of photoabsorption coefficients [Solomon et al, 2005].
    """
    def __init__(self, **kwargs):

        try:
            # Load EUV data
            self.load_euv_spectra(**kwargs)

            # Initiate species and power
            self.species = ['all', 'o', 'n2', 'o2']
            self.power = {skey: np.zeros(shape=self.year.shape)
                          for skey in self.species}
            self.bins = np.array([np.arange(5.0, 100.1, 5.0),
                                  np.arange(10.0, 105.1, 5.0)])
            self.area = {ss: None for ss in self.species}

            # Integrate power for each species
            for ss in self.species:
                self.integrate_power(species=ss)
        except FileNotFoundError:
            raise FileNotFoundError("unable to initiate EUVspectra class")

    def load_euv_spectra(self, **kwargs):
        """ Load a netCDF4 file into the EUVspectra class

        Parameters
        -----------
        file_dir : (str)
            Directory with data files (default=solar_index._data_dir)
        file_name : (str)
            Data filename (default='latest_see_L3_merged.ncdf')

        Returns
        -------
        Void
        """
        from netCDF4 import Dataset
        from os import path
        from solar_index.utilities import replace_fill_array
        from solar_index import _data_dir

        # Define default values that may be specified by kwarg
        # Done here to ensure _data_dir is defined.
        file_dir = _data_dir
        file_name = "latest_see_L3_merged.ncdf"

        for kk in kwargs.keys():
            if kk.lower() == "file_dir":
                file_dir = kwargs[kk]
            elif kk.lower() == "file_name":
                file_name = kwargs[kk]

        # Construct filename and load the data
        if not path.isdir(file_dir):
            raise Exception("unknown file directory {:s}".format(file_dir))
        self.filename = path.join(file_dir, file_name)

        if not path.isfile(self.filename):
            raise Exception("unknown file {:s}".format(self.filename))

        try:
            data = Dataset(self.filename, 'r')
        except FileNotFoundError:
            raise FileNotFoundError("unable to load netCDF4 file")

        # Assign the time data
        self.year = np.floor(data.variables['DATE'][0, :] / 1000.0).astype(int)
        self.day = np.mod(data.variables['DATE'][0, :], 1000).astype(int)
        self.dt = np.array([dt.datetime(int(self.year[i]), 1, 1) +
                            dt.timedelta(days=int(self.day[i])-1)
                            for i in range(len(self.day))])

        self.cor_1au = replace_fill_array(data.variables['COR_1AU'][0, :])
        self.He2 = replace_fill_array(data.variables['LINE_FLUX'][0, :, 1])

        self.sp_wave = replace_fill_array(data.variables['SP_WAVE'][0, :])
        self.sp_flux = replace_fill_array(data.variables['SP_FLUX'][0, :, :])
        self.line_wave = replace_fill_array(data.variables['LINEWAVE'][0, :])
        self.line_flux = replace_fill_array(data.variables['LINE_FLUX'][0, :,
                                                                        :])

    def integrate_power(self, species):
        """ Integrates EUV spectra times photoionization cross-section

        Parameters
        ----------
        species : (string)
            Specifies which species to integrate for.
            Currently supports 'o', 'n2', 'o2'

        Returns
        -------
        self.power : (dict)
            Dictionary containing the average power delivered to a given ion as
            a timeseries.
        """
        if species not in self.species:
            raise Error("unknown species")

        self.load_coeff(species=species)

        for iarea in range(len(self.area[species])):
            self.power[species] += self._integrate_bin(species, iarea)

    def _integrate_bin(self, species, iarea):
        """ Integrates sp_flux over bin values

        Parameters
        ----------
        species : (str)
        Atomic or molecular species
        iarea : (int)
        Index of the area to integrate over

        Returns
        -------
        iflux : (float)
            Integrated flux for bin
        """

        d_lambda = 1.0  # nm
        ind = (self.sp_wave >= self.bins[0, iarea]) &\
              (self.sp_wave < self.bins[1, iarea])
        iflux = self.area[species][iarea] * np.sum(self.sp_flux[:, ind],
                                                   axis=1) * d_lambda
        return iflux

    def load_coeff(self, species):
        """ Generates bins of photoabsorption coefficients using method
        described by Richards et al, 1994.

        Note: Only the wide bins are currently included, not the lines.

        Parameters
        ----------
        species : (string)
                String denoting coefficients to load (eg, 'o', 'o2', 'n2')
        """
        if species not in self.species:
            raise Error("unknown species")

        # Currently using lowest of split bins, units of square meters
        if species == 'all':
            self.area[species] = np.ones(20)
        elif species == 'o':
            self.area[species] = np.array([0.73, 1.839, 3.732, 5.202,
                                           6.461, 8.693, 9.687, 11.496,
                                           12.127, 12.059, 13.024, 13.365,
                                           17.245, 10.736, 5.091, 3.498,
                                           4.554, 1.315, 0.0, 0.0
                                           ]) * 1.0e-22
        elif species == 'n2':
            self.area[species] = np.array([0.72, 2.261, 4.958, 8.392,
                                           10.493, 13.857, 16.395, 21.675,
                                           23.471, 24.501, 22.787, 23.339,
                                           31.755, 24.662, 33.578, 16.992,
                                           20.249, 9.680, 50.988, 0.0
                                           ]) * 1.0e-22
        elif species == 'o2':
            self.area[species] = np.array([1.316, 3.806, 7.509, 10.9,
                                           14.387, 17.438, 18.118, 20.31,
                                           23.101, 24.606, 26.61, 26.017,
                                           21.919, 28.535, 22.145, 16.631,
                                           8.562, 12.817, 21.108, 1.346
                                           ]) * 1.0e-22
        else:
            raise Exception('Invalid species')

        return
