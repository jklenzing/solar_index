#!/usr/bin/env python
#---------------------------------------------------------------------------
# solarind
#
# Author: Jeff Klenzing, NASA/GSFC, August 2016
#
#
# Comments: Tools for calculating integrated solar indices.
#
# Classes: index
#
# Methods: get_index
#
#---------------------------------------------------------------------------

import numpy as np
import datetime

class SolarIndex:
	def __init__(self, file="latest_see_L3_merged.ncdf", getall=False):
		'''
		Creates index of TIMED/SEE EUV spectra

		Input:
		file	        = name of data file
		getall	        = flag to automatically load

		properties:
		'''

		from netCDF4 import Dataset


		S = Dataset(file, 'r')
		self.year  = np.floor(S.variables['DATE'][0,:]/1000)
		self.day   = np.mod(S.variables['DATE'][0,:],1000)
		self.fyear = self.year + self.day/367.0
		self.dn    = np.array([datetime.datetime(int(self.year[i]), 1, 1, 12, 0) + datetime.timedelta(days=int(self.day[i]-1)) for i in range(0,len(self.year))])

		self.cor_1au   = fix_nan(S.variables['COR_1AU'][0,:])
		self.He2       = fix_nan(S.variables['LINE_FLUX'][0,:,1])

		self.sp_wave   = fix_nan(S.variables['SP_WAVE'][0,:])
		self.sp_flux   = fix_nan(S.variables['SP_FLUX'][0,:,:])
		self.line_wave = fix_nan(S.variables['LINEWAVE'][0,:])
		self.line_flux = fix_nan(S.variables['LINE_FLUX'][0,:,:])

		self.oxygen = np.zeros(len(self.year))
		self.n2     = np.zeros(len(self.year))
		self.o2     = np.zeros(len(self.year))

		bins, area = coeff(species='o')
		for i in range(0,len(area)):
			self.oxygen = self.oxygen + integrate(bins[:,i],self.sp_wave,self.sp_flux,area[i])

		bins, area = coeff(species='n2')
		for i in range(0,len(area)):
			self.n2 = self.n2 + integrate(bins[:,i],self.sp_wave,self.sp_flux,area[i])

		bins, area = coeff(species='o2')
		for i in range(0,len(area)):
			self.o2 = self.o2 + integrate(bins[:,i],self.sp_wave,self.sp_flux,area[i])

#-- End of index

def integrate(b,x,y,s):
	'''
	Integrates sp_flux over bin values

	Input:
	b =  bounds of bins (b0, b1)
	x = wavelengths
	y = flux spectra
	s = ionization cross-section for bin of interest

	Ouput:
	iflux = Integrated flux for bin values
	'''
	d_lambda = 1.0 # nm
	ind = (x >= b[0]) & (x < b[1])
	iflux = s*np.sum(y[:,ind],axis=1)*d_lambda
	return(iflux)

#-- End of integrate

def fix_nan(x):
	'''
	Replaces missing values (-1) with nan
	'''
	x[x<0] = np.nan

	return x

#-- End of fix_nan

def coeff(species='o'):
	'''
	Generates bins of O ionization coefficients using method described by Richards et al, 1994.  Bin widths for lines taken from EUVAC code.
	Cross-sectional areas for lines taken as the difference between the published value and the wide bin in which the line resides.

	Inputs: none

	Outputs:
	bins  = coordinates of min and max of each bin
	area  = ionization cross-section (m^2)
	'''

	bins = np.array([[   5.   ,   10.   ,   15.   ,   20.   ,   25.33 ,   28.115,   25.   ,   29.831,   30.332,   30.   ,   36.507,   35.   ,
         				40.   ,   46.222,   45.   ,   50.   ,   55.131,   58.133,   55.   ,   60.676,   62.673,   60.   ,   65.   ,   70.036,
						70.   ,   76.215,   76.741,   78.636,   75.   ,   80.   ,	85.   ,   90.   ,   97.402,   95.   ,  102.272,  102.891,
					   100.],

       				 [  10.   ,   15.   ,   20.   ,   25.   ,   25.93 ,   28.715,	30.   ,   30.377,   30.678,   35.   ,   37.107,   40.   ,
         				45.   ,   46.822,   50.   ,   55.   ,   55.731,   58.733,   60.   ,   61.276,   63.273,   65.   ,   70.   ,   70.636,
         				75.   ,   76.815,   77.341,   79.236,   80.   ,   85.   ,	90.   ,   95.   ,   98.002,  100.   ,  102.872,  103.491,
         			   105.]])

	if species == 'o':
		area = np.array([ 0.73 ,   1.839,    3.732,    5.202,   -0.411,    0.619,    6.461,   -1.013,   -0.993,    8.693,    0.153,    9.687,
						 11.496,  -0.197,	12.127,   12.059,   -0.434,	   0.066,   13.024,    0.035,    0.035,   13.365,   17.245,    0.724,
						 10.736,  -1.091,	-1.201,   -1.342,    5.091,    3.498,	 4.554,	   1.315,	 0.0  ,	   0.0  ,    0.0  ,    0.0  ,
						  0.0])*1e-22 # m^2
	elif species == 'n2':
		area = np.array([ 0.72 ,   2.261,    4.958,    8.392,   -0.283,    0.407,   10.493,   -2.187,   -2.157,   13.857,    0.515,   16.395,
						 21.675,  -0.311,	23.471,   24.501,    1.343,	  -0.387,   22.787,   -0.549,    0.031,   23.339,   29.235,   10.42 ,
						 15.06 ,  51.526,	-5.774,   -5.414,   14.274,    0.0  ,	 0.0  ,	   0.0  ,	 0.0  ,	   0.0  ,    0.0  ,    0.0  ,
						 0.0])*1e-22 # m^2
	elif species == 'o2':
		area = np.array([ 1.316,   3.806,    7.509,   10.9  ,   -1.017,    1.403,   14.387,   -0.638,   -0.628,   17.438,    0.202,   18.118,
						 20.31 ,  -1.191,	23.101,   24.606,   -0.57 ,	  -3.89 ,   26.61 ,    1.453,    6.163,   24.937,   21.306,   -0.055,
						 23.805,   1.123,	-2.127,   -0.406,   10.597,    6.413,	 5.494,	   9.374,	 1.6  ,	  13.94 ,   -0.259,   -0.259,
						 0.259])*1e-22 # m^2
	else:
		raise Exception('Invalid species')

	return bins, area

#-- End of coeff_o