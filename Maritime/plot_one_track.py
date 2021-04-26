# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:32:21 2021

@author: krist
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import utillities as util
from datetime import datetime

def eta_extract_with_time(df, track_id):
    
    df = df[df['track_id'] == track_id]
    
    eta_erp = df['eta_erp'].to_numpy().astype(str)
    eta_ais = df['eta_ais'].to_numpy().astype(str)
    stamp = df['stamp'].to_numpy()
    
    idx = np.where((eta_erp != 'nan') & (eta_ais != 'nan'))
    
    eta_erp = eta_erp[idx]
    eta_ais = eta_ais[idx]
    stamp = stamp[idx]
    
    return eta_erp, eta_ais, stamp

def plot_eta_track(df, track_id):
    eta_erp, eta_ais, stamp = eta_extract_with_time(df, track_id)
    ata_ais = util.ata_Extract(df, track_id)[0]
    
    FMT = '%Y-%m-%d %H:%M:%S'
    stamp_list = []
    
    ata_ais = datetime.strptime(ata_ais, FMT)
    eta_erp = eta_erp.astype(np.datetime64) 
    eta_ais = eta_ais.astype(np.datetime64)
    
    
    for i in range(len(stamp)):
        time_before = ata_ais - datetime.strptime(stamp[i], FMT)
        stamp_list.append((time_before.days * 24 * 3600 + time_before.seconds)/3600)
        
    
    ylim_lower = np.min([eta_erp, eta_ais])
    ylim_upper = np.max([eta_erp, eta_ais])
    yrange = (ylim_upper - ylim_lower).astype('timedelta64[m]')
    ylims = (np.min([eta_erp, eta_ais]) - 0.05*yrange, 
             np.max([eta_erp, eta_ais]) + 0.05*yrange)
    
    xlim_lower = max(stamp_list)
    xlim_upper = min(stamp_list)
    xrange = xlim_lower - xlim_upper
    xlims = (xlim_lower + 0.02*xrange, xlim_upper - 0.02*xrange)
    
    
    fig, ax = plt.subplots()
    ax.plot(stamp_list, eta_erp, label='eta_erp')
    ax.plot(stamp_list, eta_ais, label='eta_ais')
    ax.hlines(ata_ais, min(stamp_list), max(stamp_list), color='k', label='ata_ais')
    ax.set_xlim(xlims)
    ax.set_ylim(ylims)
    ax.yaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
    ax.legend()
    ax.set_xlabel('Hours before arrival')
    ax.set_ylabel('Date and time')
    ax.set_title('ETA for track id: {}'.format(track_id))
    plt.subplots_adjust(left=.2)
    plt.savefig('track_plots/{}.png'.format(track_id))
    #plt.show()

df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

df = util.clean_data(df)
track_ids = df.track_id.unique()

for track_id in track_ids[:100]:
    plot_eta_track(df, track_id)
