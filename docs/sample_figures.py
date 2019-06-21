import solar_index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy

S = solar_index.EUVspectra()
F = solar_index.OMNIvals()


# Figure 1
# Oxygen photosorption cross-section as a function of wavelength
plt.plot(S.bins[0, :], S.area['o'])
plt.xlabel('Wavelength [nm]')
plt.ylabel('Photoabsorption Cross-section [m$^2$]')
plt.savefig('graphs/figure1.png')
plt.close()

# Normalization of datasets

ind1 = ~np.isnan(S.power['o'])
Opow = pd.Series(S.power['o'][ind1], index=S.dt[ind1])*1e24

ind2 = ~np.isnan(F.F107)
F107 = pd.Series(F.F107[ind2], index=F.dt[ind2])

dt = np.intersect1d(S.dt[ind1], F.dt[ind2])
df = pd.DataFrame({'F107': F107[dt], 'Opow': Opow[dt]})

window = 81

df = df.assign(Opow_mean=df['Opow'].rolling(window=window, center=True).mean())
df = df.assign(Opow_std=df['Opow'].rolling(window=window, center=True).std())
df = df.assign(Opow_nrm=(df['Opow']-df['Opow_mean'])/df['Opow_std'])

df = df.assign(F107_mean=df['F107'].rolling(window=window, center=True).mean())
df = df.assign(F107_p=(df['F107']+df['F107_mean'])/2.0)
df = df.assign(F107_std=df['F107'].rolling(window=window, center=True).std())
df = df.assign(F107_nrm=(df['F107']-df['F107_mean'])/df['F107_std'])

# Figure 2
# Timeseries of datasets

f, axarr = plt.subplots(3, sharex=True)
axarr[2].plot(df['F107_std']/df['F107_mean'], label='F10.7', color='k')
axarr[2].plot(df['Opow_std']/df['Opow_mean'], label='O power', color='r')
axarr[2].legend()

axarr[1].plot(df['F107_nrm'], label='F10.7', color='k')
axarr[1].plot(df['Opow_nrm'], label='O power', color='r')
axarr[1].legend()

axarr[0].plot(df['F107'], label='F10.7', color='k')
axarr[0].plot(df['Opow_nrm']*df['F107_std']+df['F107_mean'], label='O power',
              color='r')
axarr[0].legend()
plt.savefig('graphs/figure2.png')
plt.close()

# Figure 3
# Scatter Plot of daily values Opow vs F10.7
lower_limit = 0.05
values = (df['F107_std']/df['F107_mean'] > lower_limit) & \
         (df['Opow_std']/df['Opow_mean'] > lower_limit)

f, axarr = plt.subplots(1, 2)
axarr[0].plot(df['F107'][values], df['Opow'][values], '.k')
axarr[0].set_xlabel('F10.7 (sfu)')
axarr[0].set_ylabel('O power (yW)')

axarr[1].plot(df['F107_nrm'][values], df['Opow_nrm'][values], '.k')
axarr[1].set_xlabel('F10.7 (normalized)')
axarr[1].set_ylabel('O power (normalized)')

plt.savefig('graphs/figure3.png')
plt.close()

# Correlation coefficients of datasets

r, p = scipy.stats.pearsonr(df['F107'][values], df['Opow'][values])
ind = (~np.isnan(df['F107_nrm'])) & values
rm, pm = scipy.stats.pearsonr(df['F107_mean'][ind], df['Opow_mean'][ind])
rn, pn = scipy.stats.pearsonr(df['F107_nrm'][ind], df['Opow_nrm'][ind])

sns.jointplot('F107', 'Opow', data=df, kind="reg", size=7)
plt.savefig('graphs/figure4.png')
plt.close()

sns.jointplot('F107_nrm', 'Opow_nrm', data=df, kind="reg", size=7)
plt.savefig('graphs/figure5.png')
plt.close()

print('Correlation of raw values = %5.3f' % r)
print('Correlation of mean values = %5.3f' % rm)
print('Correlation of normalized values = %5.3f' % rn)
print([p, pm, pn])
print([len(ind), sum(ind)])
