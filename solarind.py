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

class index:
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
		self.year = np.floor(S.variables['DATE'][0,:]/1000)
		self.day  = np.mod(S.variables['DATE'][0,:],1000)
		self.fyear = self.year + self.day/367.0
		self.dn  = np.array([datetime.datetime(int(self.year[i]), 1, 1, 12, 0) + datetime.timedelta(days=int(self.day[i]-1)) for i in range(0,len(self.year))])

		self.cor_1au = fixnan(S.variables['COR_1AU'][0,:])
		self.He2 = fixnan(S.variables['LINE_FLUX'][0,:,1])
		
		self.sp_wave   = fixnan(S.variables['SP_WAVE'][0,:])
		self.sp_flux   = fixnan(S.variables['SP_FLUX'][0,:,:])
		self.line_wave = fixnan(S.variables['LINEWAVE'][0,:])
		self.line_flux = fixnan(S.variables['LINE_FLUX'][0,:,:])

		bins, area, lines, larea= coeff_o()

		self.oxygen = np.zeros(len(self.year))
		for i in range(0,len(area)):
			self.oxygen = self.oxygen + sp_int(bins[:,i],self.sp_wave,self.sp_flux,area[i])

		self.loxygen = np.zeros(len(self.year))
		for i in range(0,len(larea)):
			self.loxygen = self.loxygen + line_int(lines[i],self.sp_wave,self.sp_flux,area[i])


def sp_int(b,x,y,s):
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
	ind = (x >= b[0]) & (x < b[1])
	iflux = s*np.sum(y[:,ind],axis=1)
	return(iflux)

def line_int(line,x,y,s):
	'''
	Integrates line_flux over bin values 
	'''
	ind = np.abs(line-x)<0.1
	iflux = s*np.sum(y[:,ind],axis=1)
	return(iflux)

def fixnan(x):
	'''
	Replaces missing values (-1) with nan
	'''
	x[x==-1] = np.nan

	return x
	
def coeff_o():
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
						70.   ,   76.215,   76.741,   78.636,   75.   ,   80.   ,	85.   ,   90.   ,   97.402,   95.   ,  102.272,  102.891],
    
       				 [  10.   ,   15.   ,   20.   ,   25.   ,   25.93 ,   28.715,	30.   ,   30.377,   30.678,   35.   ,   37.107,   40.   ,
         				45.   ,   46.822,   50.   ,   55.   ,   55.731,   58.733,   60.   ,   61.276,   63.273,   65.   ,   70.   ,   70.636,
         				75.   ,   76.815,   77.341,   79.236,   80.   ,   85.   ,	90.   ,   95.   ,   98.002,  100.   ,  102.872,  103.491]])
	
	area = np.array([	 0.73 ,	   1.839,    3.732,    5.202,   -0.411,    0.619,    6.461,   -1.013,   -0.993,    8.693,    0.153,    9.687,   
						11.496,   -0.197,	12.127,   12.059,   -0.434,	   0.066,   13.024,    0.035,    0.035,   13.365,   17.245,    0.724,
						10.736,	  -1.091,	-1.201,   -1.342,    5.091,    3.498,	 4.554,	   1.315,	 0.0  ,	   0.0  ,    0.0  ,    0.0  ])*1e-22 # m^2

	lines =  np.array([25.63, 28.415, 30.331, 30.378, 36.807, 46.522, 55.437, 58.433, 60.976, 62.973, 70.336, 76.515, 77.041, 78.936])
	larea =  np.array([6.05,7.08,7.68,7.7,9.8400,11.930,12.590,13.090,13.4,13.4,11.46,4,3.89,3.749])
	
	return bins, area, lines, larea