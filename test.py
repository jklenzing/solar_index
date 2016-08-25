import numpy as np
import scipy.interpolate as sint
import matplotlib.pyplot as plt
import solarind

S = solarind.index()

omni = np.loadtxt('omni2_daily_12664.txt')
# year, doy, hour, Rz, F10.7

# Interpolate Rz and F107 to EUV measurments
ofyear = omni[:,0] + omni[:,1]/367.0 + 2/367.0
oRz   = omni[:,3]
oF107 = omni[:,4]
i = np.where(oF107>750)[0]
oF107[i] = np.nan

f = sint.interp1d(ofyear, oRz, kind='nearest', bounds_error=False, fill_value=np.nan)
S.Rz = f(S.fyear)

f = sint.interp1d(ofyear, oF107, kind='nearest', bounds_error=False, fill_value=np.nan)
S.F107 = f(S.fyear)

ind = np.where(~np.isnan(S.F107) & ~np.isnan(S.He2))[0]

print 'He2 & F10.7 => %4.2f' % np.corrcoef(S.He2[ind],S.F107[ind])[0,1]
