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

		def fixnan(x):
			'''
			Replaces missing values (-1) with nan
			'''

			x[x==-1] = np.nan

			return x
		
		S = Dataset(file, 'r')
		self.year = np.floor(S.variables['DATE'][0,:]/1000)
		self.day  = np.mod(S.variables['DATE'][0,:],1000)
		self.fyear = self.year + self.day/367.0
		self.dn  = np.array([datetime.datetime(int(self.year[i]), 1, 1, 12, 0) + datetime.timedelta(days=int(self.day[i]-1)) for i in range(0,len(self.year))])

		self.cor_1au = fixnan(S.variables['COR_1AU'][0,:])
		self.He2 = fixnan(S.variables['LINE_FLUX'][0,:,1])
		
