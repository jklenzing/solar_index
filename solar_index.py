#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2017, JK & AGB
# Full license can be found in License.md
#-----------------------------------------------------------------------------
""" Tools for calculating integrated solar indices.

Functions
-------------------------------------------------------------------------------

Classes
-------------------------------------------------------------------------------

Moduleauthor
-------------------------------------------------------------------------------
Jeff Klenzing (JK), 22 Nov 2017, Goddard Space Flight Center (GSFC)

References
-------------------------------------------------------------------------------
Richards, P.G., 1994

"""
import datetime
import numpy as np

class SolarIndex:
	""" Object containing TIMED/SEE EUV spectra and derived indices

	Parameters
	----------
	file : (string)
		name of data file to input (default='data/latest_see_L3_merged.ncdf')

	Returns
	-------
	self : SolarIndex class object containing TIMED/SEE EUV spectra
		and derived indices

	Attributes
	----------
	year : (int)
		Year of TIMED/SEE data
	day : (int)
		day of year for TIMED/SEE data
	fyear : (float)
		Fractional Years
	dn : (float)

	cor_1au : (float)
		Correction factor to 1 AU
	He2 : (float)
		HeII emission line (30.4 nm)
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

	Methods
	-------
	_integrate_bin(b,x,y,s)
		Integrates sp_flux over bin values

	_fix_nan(x)
		Replaces missing values (-1) with nan
	"""
	def __init__(self):

		self._load_file()
		self.power = dict()
		self.integrate_power(species='o')
		self.integrate_power(species='n2')
		self.integrate_power(species='o2')

	def _load_file(self, file="data/latest_see_L3_merged.ncdf"):

		from netCDF4 import Dataset

		S = Dataset(file, 'r')
		self.year  = np.floor(S.variables['DATE'][0,:]/1000)
		self.day   = np.mod(S.variables['DATE'][0,:],1000)
		self.fyear = self.year + self.day/367.0
		self.dn    = np.array([datetime.datetime(int(self.year[i]), 1, 1, 12, 0) + datetime.timedelta(days=int(self.day[i]-1)) for i in range(0,len(self.year))])

		self.cor_1au   = _fix_nan(S.variables['COR_1AU'][0,:])
		self.He2       = _fix_nan(S.variables['LINE_FLUX'][0,:,1])

		self.sp_wave   = _fix_nan(S.variables['SP_WAVE'][0,:])
		self.sp_flux   = _fix_nan(S.variables['SP_FLUX'][0,:,:])
		self.line_wave = _fix_nan(S.variables['LINEWAVE'][0,:])
		self.line_flux = _fix_nan(S.variables['LINE_FLUX'][0,:,:])

	def integrate_power(self,species):
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

		self.power[species] = np.zeros(len(self.year))

		bins, area = load_coeff(species=species)
		for i in range(0,len(area)):
			self.power[species] = self.power[species] + _integrate_bin(bins[:,i],self.sp_wave,self.sp_flux,area[i])


def _integrate_bin(b,x,y,s):
	""" Integrates sp_flux over bin values

	Parameters
	----------
	b : (float)
		bounds of bins (b0, b1)
	x : (float)
	 	wavelengths
	y : (float)
	 	flux spectra
	s : (float)
		ionization cross-section for bin of interest

	Returns
	-------
	iflux : (float)
	 	Integrated flux for bin
	"""
	d_lambda = 1.0 # nm
	ind = (x >= b[0]) & (x < b[1])
	iflux = s*np.sum(y[:,ind],axis=1)*d_lambda
	return(iflux)

def _fix_nan(x):
	""" Replaces missing values (-1) with nan

	Parameters
	----------
	x : (float)
		Value from TIMED/SEE file

	Returns
	-------
	x : (float)
	"""
	x[x<0] = np.nan

	return x


def load_coeff(species='o'):
	""" Generates bins of photoabsorption coefficients using method described
		by Solomon et al, 2005.

	Parameters
	----------
	species : (string)


	Returns
	-------
	bins : (float)
		coordinates of min and max of each bin in nm
	area : (float)
		The corresponding ionization cross-section (m^2)
	"""

	bins = np.array(
		[[	0.05,	0.4,	0.8,	1.8,	3.2,
			7.0,	15.5,	22.4,	29.0,	32.0,
			54.0,	65.0,	79.8,	91.3,	97.5,
			98.7,	102.7],

		[	0.4,	0.8,	1.8,	3.2,	7.0,
			15.5,	22.4,	29.0,	32.0,	54.0,
			65.0,	79.8,	91.3,	97.5,	98.7,
			102.7,	105.0]]
		)

	# Currently using lowest of split bins
	if species == 'o':
		area = np.array(
			[0.0023,	0.0170,		0.1125,		0.1050,		0.3247,
			 1.3190,	3.7832,		6.0239,		7.7205,		10.7175,
			 13.1253,	8.5159,		3.0031,		0.0000,		0.0000,
			 0.0000,	0.0000]
		)*1e-22 # m^2
	elif species == 'o2':
		area = np.array(
			[0.0045,	0.0340,		0.2251,		0.2101,		0.6460,
			 2.6319,	7.6283,		13.2125,	16.8233,	20.3066,
			 27.0314,	23.5669,	10.4980,	13.3950,	18.7145,
			 1.6320,	1.1500]
		)*1e-22 # m^2
	elif species == 'o2':
		area = np.array(
			[0.0025,	0.0201,		0.1409,		1.1370,		0.3459,
			 1.5273,	5.0859,		9.9375,		11.7383,	19.6514,
			 23.0931,	23.0346,	2.1434,		2.1775,		2.5465,
			 0.0000,	0.0000]
		)*1e-22 # m^2
	else:
		raise Exception('Invalid species')

	return bins, area
