#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------
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
import logbook as logging

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
            self.species = ['o', 'n2', 'o2']
            self.power = {skey:np.zeros(shape=self.year.shape)
                          for skey in self.species}
            self.bins = np.array([[0.05, 0.4, 0.8, 1.8, 3.2, 7.0, 15.5, 22.4,
                                   29.0, 32.0, 54.0, 65.0, 79.8, 91.3, 97.5,
                                   98.7, 102.7],
                                  [0.4, 0.8, 1.8, 3.2, 7.0, 15.5, 22.4, 29.0,
                                   32.0, 54.0, 65.0, 79.8, 91.3, 97.5, 98.7,
                                   102.7, 105.0]])
            self.area = {ss:None for ss in self.species}

            # Integrate power for each species
            for ss in self.species:
                self.integrate_power(species=ss)
        except:
            logging.error("unable to initiate EUVspectra class")


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
                self._file_name = kwargs[kk]

        # Construct filename and load the data
        assert path.isdir(file_dir), \
            logging.error("unknown file directory {:s}".format(file_dir))
        self.filename = path.join(file_dir, file_name)

        assert path.isfile(self.filename), \
            logging.error("unknown file {:s}".format(self.filename))

        try:
            data = Dataset(self.filename, 'r')
        except:
            logging.error("unable to load netCDF4 file")

        # Assign the time data
        self.year = np.floor(data.variables['DATE'][0,:] / 1000.0).astype(int)
        self.day = np.mod(data.variables['DATE'][0,:], 1000).astype(int)
        self.dt = np.array([dt.datetime(int(self.year[i]),1,1) +
                            dt.timedelta(days=int(self.day[i])-1)
                            for i in range(len(self.day))])

        self.cor_1au = replace_fill_array(data.variables['COR_1AU'][0,:])
        self.He2 = replace_fill_array(data.variables['LINE_FLUX'][0,:,1])

        self.sp_wave = replace_fill_array(data.variables['SP_WAVE'][0,:])
        self.sp_flux = replace_fill_array(data.variables['SP_FLUX'][0,:,:])
        self.line_wave = replace_fill_array(data.variables['LINEWAVE'][0,:])
        self.line_flux = replace_fill_array(data.variables['LINE_FLUX'][0,:,:])


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
        assert species in self.species, logging.error("unknown species")

        self.load_coeff(species=species)

	for iarea in range(len(self.area[species])):
	    self.power[species] += self.power[species] + \
                                   self._integrate_bin(species, iarea)


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

        d_lambda = 1.0 # nm
	ind = (self.sp_wave >= self.bins[0,iarea]) & (self.sp_wave
                                                      < self.bins[1,iarea])
	iflux = self.area[species][iarea] * np.sum(self.sp_flux[:,ind],
                                                   axis=1) * d_lambda
	return iflux


    def load_coeff(self, species):
        """ Generates bins of photoabsorption coefficients using method
        described by Solomon et al, 2005.

        Parameters
        ----------
        species : (string)
                String denoting coefficients to load ('o', 'o2', 'n2' supported)
        """
        assert species in self.species, logging.error("unknown species")

        # Currently using lowest of split bins, units of square meters
        if species == 'o':
            self.area[species] = np.array([0.0023, 0.0170, 0.1125, 0.1050,
                                           0.3247, 1.3190, 3.7832, 6.0239,
                                           7.7205, 10.7175, 13.1253, 8.5159,
                                           3.0031, 0.0000, 0.0000, 0.0000,
                                           0.0000]) * 1.0e-22
        elif species == 'o2':
            self.area[species] = np.array([0.0045, 0.0340, 0.2251, 0.2101,
                                           0.6460, 2.6319, 7.6283, 13.2125,
                                           16.8233, 20.3066, 27.0314,
                                           23.5669, 10.4980, 13.3950, 18.7145,
                                           1.6320, 1.1500]) * 1.0e-22
        elif species == 'n2':
            self.area[species] = np.array([0.0025, 0.0201, 0.1409, 1.1370,
                                           0.3459, 1.5273, 5.0859, 9.9375,
                                           11.7383, 19.6514, 23.0931, 23.0346,
                                           2.1434, 2.1775, 2.5465, 0.0000,
                                           0.0000]) * 1.0e-22
        else:
            raise Exception('Invalid species')

        return
