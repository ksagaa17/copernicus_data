# -*- coding: utf-8 -*-
"""
Created on Sun May  2 15:44:42 2021

@author: krist
"""

import utillities as ut
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

pardir = os.path.dirname(os.getcwd())
df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
#df = pd.read_csv("Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
df = ut.clean_data(df)

track_ids = df.track_id.unique()

track_id = track_ids[0]
ata = ut.ata_Extract(df, track_id).astype('datetime64[s]')
erp, ais = ut.eta_Extract_whole_track(df, track_id)
erp = erp.astype('datetime64[s]')
ais = ais.astype('datetime64[s]')

ais_diff = np.abs(ata - ais)

def time_difference_array(time1, time2):
    """
    Computes the absolute difference between two arrays of datetimes and 
    returns an array absolute differences in seconds.

    Parameters
    ----------
    time1 : ndarray, datetime64 or str
        Array of datetimes.
    time2 : ndarray, datetime64 or str
        Array of datetimes. Must have length 1 or len(time1).

    Returns
    -------
    time1 : ndarray, timedelta64[s]
        Array of time differences in seconds.

    """
    time1 = time1.astype('datetime64[s]')
    time2 = time2.astype('datetime64[s]')
    
    try:
        diff = np.abs(time1 - time2)
        return(diff)
    
    except ValueError:
        print("time2 must either have same length as time1 or have a length of 1. " +
              "time2 has length {}".format(len(time2)))
    
    

ais_diff2 = time_difference_array(ais, erp)
