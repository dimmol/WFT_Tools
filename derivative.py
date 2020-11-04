# -*- coding: utf-8 -*-
"""
Created on Sun Nov  1 21:38:22 2020

@author: molok
"""

import pandas as pd
# import datetime as dt


df = pd.read_csv('./LAS/XPT_HRLA_TLD_MCFL_037LTP.las', delim_whitespace=True, 
                 header=None, skiprows=67, usecols=[11,16], 
                 names=['ETIM', 'QCP'])

df['Der'] = df['QCP'].diff()/df['ETIM'].diff()
df['Der'].fillna(0, inplace=True)
# df['Der'] = df['Der']*10
df['Der2'] = df['Der'].diff()/df['ETIM'].diff()
df['Der2'].fillna(0, inplace=True)
df['Flag'] = df['Der'].apply(lambda x: 0 if abs(x)<5 else 1)

df['Cons'] = df.Flag.groupby((df.Flag != df.Flag.shift()).cumsum()).transform('size')
df.Cons.loc[df['Cons']<30]=None
df.Cons.fillna(method='backfill', inplace=True)
df['#']=df.Cons.factorize()[0]+1
# EPOCH = dt.datetime.now()

# df['Fake_time'] = df['ETIM'].map(lambda x: EPOCH+dt.timedelta(seconds=x))
# df.set_index('Fake_time', inplace=True)
# # df = df.resample('1S')

# der = df['QCP'].diff()/df.index.to_series().diff().dt.total_seconds()

# der = der.reset_index()
ax = df.plot(x='ETIM', y='Der')
ax = df['#'].plot(secondary_y=True)
# ax.set_xlim(150, 250)
# fig = ax.get_figure()
# ax = fig.get_axes()
# ax[1].set_ylim(0,3)

mud_before = df[df['#']==df['#'].min()]['QCP'].mean()
mud_after = df[df['#']==df['#'].max()]['QCP'].mean()

# hist = df.hist(column='QCP', bins=500)
# hist[0][0].set_xlim(5800, 5900)
# print(hist[0])
# print(der.head())
# print(df.head(20))
# print(mean_vals)
print(df[df['#']==df['#'].max()-1].index[0])
print(df[df['#']==df['#'].max()].index[0]-1)
print(df[df['#']==df['#'].max()-1].ETIM.min())
print(df[df['#']==df['#'].max()-1].ETIM.max())
print(df[df['#']==df['#'].max()-1].QCP.max())
print(df[df['#']==df['#'].max()-1].QCP.min())

# print(mud_before)