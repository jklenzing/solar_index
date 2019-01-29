[![Build Status](https://travis-ci.com/jklenzing/solar_index.svg?branch=master)](https://travis-ci.com/jklenzing/solar_index)
[![Coverage Status](https://coveralls.io/repos/github/jklenzing/solar_index/badge.svg?branch=master)](https://coveralls.io/github/jklenzing/solar_index?branch=master)
[![DOI](https://zenodo.org/badge/111730061.svg)](https://zenodo.org/badge/latestdoi/111730061)

alpha version.  Use with caution!

The solar_index package is designed to compare various proxies and measurements
for solar activity, such as sunspot number and F10.7, over a variety of
timescales ranging from days to years.  Additionally, the use of several
proxies calculated from solar EUV measurements will be incorporated in the
future.

# Indices Currently Supported
* OMNIvals
  * Rz - daily sunspot number
  * F10.7 - Flux of 10.7 cm radiation (sfu)
  * Lyman alpha
* EUVspectra
  * EUV spectra (0.5-194.5 nm) from TIMED/SEE (http://lasp.colorado.edu/home/see/data/)
  * Integrated power of EUV from 5-105 nm (S.power['all'])

The alpha version was developed as a "proof-of-concept" for comparing the day-
to-day variability of commonly used solar indices with measured EUV spectra
for use in driving upper atmospheric models.

The beta version of this code (in development) will reorganize using pysat to
allow the indices to be updated rather than hard-coded.  Additionally, more
proxies will be added.  Please contact the code author regarding questions.
