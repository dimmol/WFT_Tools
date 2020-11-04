# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:15:50 2020

@author: Dmitry Molokhov
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches

df = pd.read_csv('./LAS/XPT_HRLA_TLD_MCFL_037LTP.las', delim_whitespace=True, 
                 header=None, skiprows=67, usecols=[0,3,11,16], 
                 names=['Time', 'Depth', 'ETIM', 'QCP'])

lim1 = [500, 5400]
lim2 = [750, 5600]

lim3 = [700, 5501.6]
lim4 = [740, 5501.7]

pres = 5501.65

plt.style.use('ggplot')

plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = 'Ubuntu'
plt.rcParams['font.monospace'] = 'Ubuntu Mono'
plt.rcParams['font.size'] = 8
plt.rcParams['axes.labelsize'] = 8
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['axes.titlesize'] = 10
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['figure.titlesize'] = 12

fig = plt.figure(figsize=(8.5, 5.5), dpi=800)
fig.subplots_adjust(hspace=0.25)
fig.suptitle("Pressure test at "+str(round(df.iloc[1]['Depth'], 2)) +"m MD")

gs = plt.GridSpec(2, 2, height_ratios = [3,1])

ax1 = plt.subplot(gs[0, :])

ax1.plot(df['ETIM'], df['QCP'])
plt.xlabel('Ellapsed Time (s)')
plt.ylabel('Quartz Gauge Pressure (psia)')
rect = patches.Rectangle((lim1[0], lim1[1]), lim2[0]-lim1[0], lim2[1]-lim1[1], linewidth=0.5, edgecolor='k', 
                         linestyle='--', facecolor='none')
ax1.add_patch(rect)
ax1.text(lim1[0], lim2[1], 'Zoom 1', horizontalalignment='left', verticalalignment='bottom')

# Plot #2

ax2 = plt.subplot(gs[1, 0])

ax2.plot(df['ETIM'], df['QCP'])
plt.xlabel('Ellapsed Time (s)')
plt.ylabel('Quartz Gauge Pressure (psia)')
plt.xlim(lim1[0], lim2[0])
plt.ylim(lim1[1], lim2[1])
rect = patches.Rectangle((lim3[0], lim3[1]-10), lim4[0]-lim3[0], 20, linewidth=0.5, edgecolor='k', 
                         linestyle='--', facecolor='none')
ax2.add_patch(rect)
ax2.text(lim3[0], lim4[1]+10, 'Zoom 2', horizontalalignment='left', verticalalignment='bottom')
ax2.set_title("Zoom 1")

# Plot #3

ax3 = plt.subplot(gs[1, 1])

ax3.plot(df['ETIM'], df['QCP'])
ax3.plot([lim3[0]*1.05, lim4[0]*0.95], [pres, pres], color='k', linestyle='--', linewidth=2)
ax3.text((lim3[0]+lim4[0])/2, pres, str(pres)+' psia', horizontalalignment='left', verticalalignment='bottom')
plt.xlabel('Ellapsed Time (s)')
# plt.ylabel('Quartz Gauge Pressure (psia)')
plt.xlim(lim3[0], lim4[0])
plt.ylim(lim3[1], lim4[1])
ax3.set_title("Zoom 2")

fig.tight_layout()

plt.show()

print(df.head())