import numpy as np
import scipy.interpolate as sint
import matplotlib.pyplot as plt
from solar_index import SolarIndex
import seaborn
import datetime

S = SolarIndex()

omni = np.loadtxt('data/omni2_daily_12664.txt')
# year, doy, hour, Rz, F10.7

# Interpolate Rz and F107 to EUV measurments
ofyear  = omni[:,0] + omni[:,1]/367.0 + 2/367.0
oRz     = omni[:,3]
oF107   = omni[:,4]
oLalpha = omni[:,5]
i = np.where(oF107>750)[0]
oF107[i] = np.nan

f = sint.interp1d(ofyear, oRz, kind='nearest', bounds_error=False, fill_value=np.nan)
S.Rz = f(S.fyear)

f = sint.interp1d(ofyear, oF107, kind='nearest', bounds_error=False, fill_value=np.nan)
S.F107 = f(S.fyear)

ind = ~np.isnan(S.F107) & ~np.isnan(S.power['o'])

print('Oxygen Cross Section & F10.7 => %4.2f' % np.corrcoef(S.power['o'][ind],S.F107[ind])[0,1])

for year in range(2003,2017):
	jnd = np.logical_and(ind, S.year==year)
	print('%d => %4.2f' % (year, np.corrcoef(S.power['o'][jnd],S.F107[jnd])[0,1]))

jnd = np.logical_and(S.year<=2012,S.F107<200)
p = np.polyfit(S.F107[np.logical_and(ind,jnd)],S.power['o'][np.logical_and(ind,jnd)]*1e24,2)
x = range(70,201)
y = np.polyval(p,x)

jnd = S.year<=2012
fig = plt.figure(figsize=(6,8))
plt.plot(S.F107[np.logical_and(ind,jnd)],S.power['o'][np.logical_and(ind,jnd)]*1e24,'.k')
plt.plot(x,y,'r',linewidth=2)
plt.xlabel('F10.7 (sfu)', fontsize=16)
plt.ylabel('Oxygen Power (yW)', fontsize=16)
plt.title('2002 - 2012')
plt.savefig('tests/Solar Indices.png')
plt.close('all')

jnd = np.logical_and(S.year<=2012,S.F107<200)
p = np.polyfit(S.F107[np.logical_and(ind,jnd)],S.He2[np.logical_and(ind,jnd)]*1e6,2)
x = range(70,201)
y = np.polyval(p,x)

jnd = S.year<=2012
fig = plt.figure(figsize=(6,8))
ax = fig.add_subplot(1,1,1)
plt.plot(S.F107[np.logical_and(ind,jnd)],S.He2[np.logical_and(ind,jnd)]*1e6,'.k')
plt.plot(x,y,'r',linewidth=2)
plt.xlabel('F10.7 (sfu)', fontsize=16)
ax.tick_params(axis='both', which='major', labelsize=14)
plt.xlim([50,250])
plt.ylim([200,500])
plt.ylabel('30.4 nm radiation flux ($\mu$W/m$^2$/nm)', fontsize=16)
plt.title('TIMED/SEE data (2002-2012)',fontsize=20)
plt.savefig('tests/He2.png')
plt.close('all')



#fig = plt.figure(figsize=(25,4))
#fig.subplots_adjust(left = 0.03, right = 0.97, bottom = 0.15, top = 0.9)

#ax1 = fig.add_subplot(111)
#line1 = ax1.plot(S.dn,S.oxygen*1e24,'-r')
#plt.ylim(np.polyval(p,[50,250]))
#plt.ylabel('Oxygen Power (yW)', fontsize=16, color='r')

#ax2 = fig.add_subplot(111, sharex=ax1, frameon=False)
#line2 = ax2.plot(S.dn,S.F107,'--k')
#ax2.yaxis.tick_right()
#ax2.yaxis.set_label_position("right")
#plt.ylabel('F10.7 (sfu)', fontsize=16)
#plt.ylim([50,250])


#plt.savefig('tests/time.png')
#plt.close('all')

fig = plt.figure(figsize=(16,16))
fig.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)

yrange = [2002,2007]
i = 0
for year in range(yrange[0],yrange[1]):
	i = i+1
	fig.add_subplot(np.diff(yrange),1,i)
	jnd  = S.year==year
	q0   = np.mean(S.power['o'][np.logical_and(ind,jnd)])
	qsig = np.std(S.power['o'][np.logical_and(ind,jnd)])
	f0   = np.mean(S.F107[np.logical_and(ind,jnd)])
	fsig = np.std(S.F107[np.logical_and(ind,jnd)])
	q = plt.plot(S.dn[jnd],(S.power['o'][jnd]-q0)/qsig,'r',label = '<O$_{pow}$>')
	f = plt.plot(S.dn[jnd],(S.F107[jnd]-f0)/fsig,'k',label = 'F10.7')
	plt.xlim([datetime.datetime(year,1,1),datetime.datetime(year+1,1,1)])
	if i==1:
		plt.legend(loc="upper left")

plt.suptitle('Comparison of Solar Indices - Average Oxygen Power vs F10.7',fontsize=16)
plt.savefig('tests/2002-2008.png')
plt.close('all')

fig = plt.figure(figsize=(16,16))
fig.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.05, top = 0.95)

yrange = [2007,2013]
i = 0
for year in range(yrange[0],yrange[1]):
	i = i+1
	fig.add_subplot(np.diff(yrange),1,i)
	jnd  = S.year==year
	q0   = np.mean(S.power['o'][np.logical_and(ind,jnd)])
	qsig = np.std(S.power['o'][np.logical_and(ind,jnd)])
	f0   = np.mean(S.F107[np.logical_and(ind,jnd)])
	fsig = np.std(S.F107[np.logical_and(ind,jnd)])
	q = plt.plot(S.dn[jnd],(S.power['o'][jnd]-q0)/qsig,'r',label = '<O$_{pow}$>')
	f = plt.plot(S.dn[jnd],(S.F107[jnd]-f0)/fsig,'k',label = 'F10.7')
	plt.xlim([datetime.datetime(year,1,1),datetime.datetime(year+1,1,1)])
	if i==1:
		plt.legend(loc="upper left")

plt.suptitle('Comparison of Solar Indices - Average Oxygen Power vs F10.7',fontsize=16)
plt.savefig('tests/2009-2016.png')
plt.close('all')
