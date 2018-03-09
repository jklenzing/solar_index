import solar_index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn

S = solar_index.EUVspectra()
F = solar_index.OMNIvals()

ind = ~np.isnan(S.power['o'])
Opow = pd.DataFrame(S.power['o'][ind], index=S.dt[ind])

ind = ~np.isnan(F.F107)
F107 = pd.DataFrame(F.F107[ind], index=F.dt[ind])

window = 81

Opow_mean = Opow.rolling(window=window,center=True).mean()
Opow_std = Opow.rolling(window=window,center=True).std()
Opow_nrm = (Opow-Opow_mean)/Opow_std

F107_mean = F107.rolling(window=window,center=True).mean()
F107_std = F107.rolling(window=window,center=True).std()
F107_nrm = (F107-F107_mean)/F107_std

plt.plot(F107_nrm, label='F10.7')
plt.plot(Opow_nrm, label='O power')
plt.legend()
plt.show()
