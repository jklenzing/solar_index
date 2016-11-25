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

ind = ~np.isnan(S.F107) & ~np.isnan(S.oxygen)

print 'Oxygen Cross Section & F10.7 => %4.2f' % np.corrcoef(S.oxygen[ind],S.F107[ind])[0,1]

for year in range(2003,2017):
	jnd = np.logical_and(ind, S.year==year)
	print '%d => %4.2f' % (year, np.corrcoef(S.oxygen[jnd],S.F107[jnd])[0,1])

p = np.polyfit(S.F107[ind],S.oxygen[ind]*1e24,2)
x = range(70,201)
y = np.polyval(p,x)

plt.plot(S.F107[ind],S.oxygen[ind]*1e24,'.k')
plt.hold(True)
plt.plot(x,y,'r',linewidth=2)
plt.xlabel('F10.7 (sfu)', fontsize=16)
plt.ylabel('Oxygen Power (yW)', fontsize=16)
plt.title('2002 - 2015')
plt.show()

