# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 15:32:21 2021

@author: krist
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time_func as tf
import extract_function as clean
from datetime import datetime

def eta_extract_with_time(df, track_id):
    #indexes = df.query('track_id == {0}'.format(track_id)).index
    
    # Virker ikke endnu, mangler at virker for andet en første track id
    
    df = df[df['track_id'] == track_id]
    
    eta_erp = df['eta_erp'].to_numpy().astype(str)
    eta_ais = df['eta_ais'].to_numpy().astype(str)
    stamp = df['stamp'].to_numpy()
    
    idx = np.where((eta_erp != 'nan') & (eta_ais != 'nan'))
    
    eta_erp = eta_erp.loc[idx]
    eta_ais = eta_ais.loc[idx]
    stamp = stamp.loc[idx]
    

    
    
    return eta_erp, eta_ais, stamp

def plot_eta_track(df, track_id):
    eta_erp, eta_ais, stamp = eta_extract_with_time(df, track_id)
    ata_ais = tf.ata_Extract(df, track_id)[0]
    
    FMT = '%Y-%m-%d %H:%M:%S'
    eta_erp_list = []
    eta_ais_list = []
    stamp_list = []
    
    ata_ais = datetime.strptime(ata_ais, FMT)
    
    for i in range(len(stamp)):
        eta_erp_list.append(datetime.strptime(eta_erp[i], FMT))
        eta_ais_list.append(datetime.strptime(eta_ais[i], FMT))
        time_before = ata_ais - datetime.strptime(stamp[i], FMT)
        stamp_list.append((time_before.days * 24 * 3600 + time_before.seconds)/3600)
        
        
    plt.figure()
    plt.plot(stamp_list, eta_erp_list, label='eta_erp')
    plt.plot(stamp_list, eta_ais_list, label='eta_ais')
    plt.hlines(ata_ais, min(stamp_list), max(stamp_list), color='k', label='ata_ais')
    plt.xlim(max(stamp_list), min(stamp_list))
    plt.legend()
    plt.xlabel('Hours before arrival')
    plt.ylabel('Date and hour')
    plt.show()

df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

df = clean.clean_data(df)
track_ids = df.track_id.unique()

for track_id in track_ids[:1]:
    plot_eta_track(df, track_id)
