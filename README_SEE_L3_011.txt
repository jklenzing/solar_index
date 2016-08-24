README file for:
----------------
TIMED SEE Level 3 Data Products

This README file is located at:
ftp://laspftp.colorado.edu/pub/SEE_Data/level3/README_SEE_L3_011.TXT

Also read the SEE_v11_releasenotes.txt file for known issues 
with the SEE data at:
ftp://laspftp.colorado.edu/pub/SEE_Data/SEE_v11_releasenotes.txt

--------------------------------------------------
TIMED Data Rules of the Road & Data Access Policy
--------------------------------------------------
Users of TIMED data are asked to respect the following 
guidelines

Mission scientific and model results are open to all.

Users should contact the PI or designated team member of an 
instrument or modeling group early in an analysis project 
to discuss the appropriate use of instrument data or model 
results. This applies to TIMED mission team members, guest 
investigators, and other members of the scientific 
community or general public.

Users that wish to publish the results derived from TIMED 
data should normally offer co-authorship to the PI or 
his/her designated team member.  Co-authorship may be 
declined. Appropriate acknowledgement to institutions, 
personnel, and funding agencies should be given.

Users should heed the caveats of investigators as to the 
interpretation and limitations of data or model results. 
Investigators supplying data or models may insist that such 
caveats be published, even if co-authorship is declined. 
Data and model version numbers should also be specified

Pre-prints of publications and conference abstracts should 
be widely distributed to interested parties within the 
mission and related projects.

See also: http://www.timed.jhuapl.edu/scripts/mdc_rules.pl


--------------------------------------------------
TIMED SEE Level 3 Data Product
--------------------------------------------------

SEE Level 3 OVERVIEW:  The Solar EUV Experiment (SEE) is comprised
of two science components: 

the EUV Grating Spectrograph (EGS) component covers the wavelength 
range from approximately 26 to 190 nm (see EGS Level 2 notes below)

the X-Ray Photometer System (XPS) component covers the wavelength 
range from approximately 0.5 to 34 nm (see XPS Level 2 notes below).

Details of the instrument can be found at 
http://lasp.colorado.edu/see/see_instrument.html

SEE Level 3 data files contain one daily averaged solar irradiance 
spectrum in 1 nm intervals extracted from the EGS Level 2 and XPS 
Level 2 data products. Shortward of 27 nm, a solar model is scaled 
to match the XPS broadband data. SEE Level 3 data files also contain 
38 emission lines extracted from EGS Level 2 spectra, and the XPS 
Level 2 diode irradiances.

For normal operations, SEE observes the Sun for about 3 minutes 
every orbit (97 minutes), which usually gives 14-15 measurements 
per day. The SEE Level 3 data are time averaged over the entire 
day, after applying corrections for atmospheric absorption, 
degradation, flare removal, and to 1-AU. A suborbital (sounding 
rocket) payload is flown approximately once a year for TIMED SEE 
absolute calibrations.  The first SEE suborbital calibration flight was 
on Feb. 8, 2002, the second was on Aug. 12, 2003, the third was
on Oct. 15, 2004, the fourth was on Oct. 28, 2006, and the final
SEE calibration flight was on Apr. 14, 2008.  There are also three
SDO EVE calibration flights used for checking SEE degradation trends -
May 3, 2010, Mar. 23, 2011, and June 23, 2012.

DATA LOCATION:  SEE FTP site at
          ftp://laspftp.colorado.edu/pub/SEE_Data/level3/

  Copy the *.ncdf files as BINARY files.

  Copy the *.pro files (IDL procedures) as ASCII files.

  Copy the *.txt files (help files) as ASCII files.

  A special mission-to-date merged file is created from this data
  and updated daily. The most recent file may be located at:
  ftp://laspftp.colorado.edu/pub/SEE_Data/level3/
  with a naming convention of see__L3_merged_YYYYDOY_011.ncdf

FILE FORMAT:  NetCDF file for each daily average

FILE CONTENT:  Solar irradiance from 0.5-190 nm gridded onto 
1-nm bins.

CURRENT VERSION:  11 (released 10/12)

SEE_v11_releasenotes.txt for more details.

READING A FILE:  
You can use the IDL procedure read_netcdf.pro to read the 
SEE data products (or almost any NetCDF file).  Example 
usage follows.

  IDL> read_netcdf,'see__L3_2002039_011_01.ncdf',d,att
where
  d = data read from the specified file
  att = string array listing the attributes (definitions)

  IDL> help, d, /structure    ; to list data structure

  IDL> n = n_elements(att)		; to print attributes
  IDL> for k=0,n-1 do print, att[k]

read_netcdf.pro can be found at
ftp://laspftp.colorado.edu/pub/see/software/idl/netCDF/read_netcdf.pro

--------------------------------------------------
Special Software for Level 3 Data Products
--------------------------------------------------

PLOT_SEE.PRO
--------------
This procedure will plot a time series (TS) for a 
specified line, or wavelength bin, or plot a spectrum
for a given day, or plot an xps diode time series.

  IDL> plot_see, /list_lines ; lists the 38 line numbers
  IDL> plot_see, line_num=23 ; plots a time series for C III 97.7 nm
  IDL> plot_see,30,data=d,type='TS' ;plot time series of bin at 30 nm
  IDL> plot_see, xps_num=1   ; plots xps diode 1 time series
  IDL> plot_see,2002039,data=d,type='SP' ;plot the spectrum for one day

plot_see.pro can be found at
ftp://laspftp.colorado.edu/pub/SEE_Data/level3/plot_see.pro


--------------------------------------------------
Version History for SEE Level 3 Data Product
--------------------------------------------------
1.00  Pre-launch test version

2.00  Pre-launch revised test version

3.00  12/01  Early-operation version

4.00   5/02  Not a publicly available version. 

5.00   9/02  Not a publicly available version.

6.00   3/03  First public version.

7.00   7/04  See SEE_v7_releasenotes.txt for information.

8.00   6/05  See SEE_v8_releasenotes.txt for information.

9.00   4/07  See SEE_v9_releasenotes.txt for information.

10.00  7/09  See SEE_v10_releasenotes.txt for information.

11.00  10/12 See SEE_v11_releasenotes.txt for information.

--------------------------------------------------

The main SEE web page is:  http://lasp.colorado.edu/see

For SEE data access problems or suggestions, you can send 
e-mail to don.woodraska@lasp.colorado.edu or 
tom.woods@lasp.colorado.edu

--------------------------------------------------
END OF README FILE
