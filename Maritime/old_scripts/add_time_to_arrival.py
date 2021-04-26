# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 17:01:20 2021

@author: krist
"""

import numpy as np
import pandas as pd
import time_func as tf

def add_hours_bef_arr(df):
    track_ids = df.track_id.unique()
    hours_bef_arrive = np.zeros(0)
    for track_id in track_ids:
        df_small = df.loc[df['track_id']==track_id]
        stamp = df_small['stamp'].to_numpy().astype('datetime64[s]')
        ata = tf.ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
        diff = (ata - stamp).astype('timedelta64[h]')
        hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
    
    df['hours_bef_arr'] = hours_bef_arrive
    return df

if __name__ == "__main__":
    df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                  'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    
    df = tf.clean_data(df)
    df = add_hours_bef_arr(df)
