import solar_index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

S = solar_index.EUVspectra()
F = solar_index.OMNIvals()


#### Figure 1
plt.plot(S.bins[0,:],S.area['o'])
plt.xlabel('Wavelength [nm]')
plt.ylabel('Photoabsorption Cross-section [m$^2$]')
plt.savefig('SW2018graphs/figure1.png')
plt.close()

#### Normalization of datasets

ind1 = ~np.isnan(S.power['o'])
Opow = pd.Series(S.power['o'][ind1], index=S.dt[ind1])

ind2 = ~np.isnan(F.F107)
F107 = pd.Series(F.F107[ind2], index=F.dt[ind2])

dt = np.intersect1d(S.dt[ind1],F.dt[ind2])
df = pd.DataFrame({'F10.7':F107[dt], 'Opow':Opow[dt]})

window = 81

Opow_mean = df['Opow'].rolling(window=window,center=True).mean()
Opow_std = df['Opow'].rolling(window=window,center=True).std()
Opow_nrm = (df['Opow']-Opow_mean)/Opow_std

F107_mean = df['F10.7'].rolling(window=window,center=True).mean()
F107_p = (df['F10.7']+F107_mean)/2.0
F107_std = df['F10.7'].rolling(window=window,center=True).std()
F107_nrm = (df['F10.7']-F107_mean)/F107_std

#### Figure 2
plt.ion()
f, axarr = plt.subplots(3, sharex=True)
axarr[2].plot(F107_std/F107_mean, label='F10.7', color = 'k')
axarr[2].plot(Opow_std/Opow_mean, label='O power', color='r')
axarr[2].legend()

axarr[1].plot(F107_nrm, label='F10.7', color = 'k')
axarr[1].plot(Opow_nrm, label='O power', color='r')
axarr[1].legend()

axarr[0].plot(df['F10.7'], label='F10.7', color = 'k')
axarr[0].plot(Opow_nrm*F107_std+F107_mean, label='O power', color='r')
axarr[0].legend()

#### Correlation coefficients of datasets

lower_limit = 0.05

values = (F107_std/F107_mean>lower_limit) & (Opow_std/Opow_mean>lower_limit)
r,p = scipy.stats.pearsonr(df['F10.7'][values],df['Opow'][values])
ind = (~np.isnan(F107_nrm)) & values
rm,pm = scipy.stats.pearsonr(F107_mean[ind],Opow_mean[ind])
rn,pn = scipy.stats.pearsonr(F107_nrm[ind],Opow_nrm[ind])

print('%5.3f  %5.3f  %5.3f' % (r,rm,rn))
print([p,pm,pn])
print([len(ind),sum(ind)])

#### Time Lag Analysis
