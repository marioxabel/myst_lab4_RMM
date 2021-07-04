#%%
# -- import libraries
import pandas as pd
import numpy as np
import datetime
matplotlib as plot

# -- import project scripts
import functions_PyMetatrader5 as fnmt5
#%%
local_exe = 'C:\\Program Files\\MetaTrader 5\\terminal64.exe'
#local_exe = 'C:\\Archivos de programa\\MetaTrader 5 Terminal\\terminal64.exe'
# construct a datetime that is explicitly aware of the difference Fechas de descarga
ini_date = datetime.datetime(2021, 6, 22, 1, 0)
end_date = datetime.datetime(2021, 6, 23, 0, 0)


# Cuenta Renatta
# account number 
mt5_acc_Renatta = 5383442
# account pass
mt5_inv_pas_Renatta = "44GxKTtf"
# try initialization and login
mt5_client = fnmt5.f_init_login(mt5_acc_Renatta, mt5_inv_pas_Renatta , local_exe)

# %%
hist_mt5 = fnmt5.f_hist_prices(mt5_client, ['EURUSD'], 'M1',ini_date,
                                                   end_date).get('EURUSD')
hist_mt5['time'] = hist_mt5['time'].apply(datetime.datetime.fromtimestamp)
# %%
hist_mt5.to_csv('prices.csv')

# %%


# Dataframe con diff
data = hist_mt5.loc[:,['time','close']] 
data['diff'] = data['close']-data['close'].shift(1)
data['diff2'] = data['close']-data['close'].shift(2)

data.dropna(inplace=True)


# %%
# calculo de C
c = - np.sqrt((data['diff']*data['diff2']).mean())
sigma = np.var(data['diff']) - 2*c**2

data['ask']= data['close'] + np.abs(c)
data['bid']= data['close'] - np.abs(c)

# %%
data.loc[:, ['bid', 'ask']].plot()
# %%
