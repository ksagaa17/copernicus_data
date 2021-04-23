# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 17:06:26 2021

"""

import pandas as pd
import numpy as np
import math

def clean_data(df):
    """
    Clean data. I loggen er der nogle stamps som ikke er relavante ifm at beregne
    performance af ETA1 algoritmen. fx er der skibe som kun har ankomsttid og skibe
    som ikke er ankommet endnu. Derudover er ankomst tiden gentaget mange gange i loggen.
    Ydermere er der nogle eksempler på skibe som hverken har eta_ais eller eta_ais.
    Alt dette overkydende data fjernes med denne funktion. 

    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.

    Returns
    -------
    df : pandas dataframe
        Cleaned log.

    """
    # remove ships that has not arrived
    df_arrive = df[df['status'] == 14]
    df = df[df['track_id'].isin(df_arrive['track_id'])]
    
    # remove ships that only has status 14 in the log
    df_eta = df[df['status'] != 14]
    df = df[df['track_id'].isin(df_eta['track_id'])]
    df = df.sort_values(by=['track_id', 'stamp'])
    
    
    # Look at one track
    df_first_track = df[df['track_id'] == df['track_id'].to_numpy()[0]]
    df_first_track = df_first_track.sort_values(by=['stamp'])
    # df_first_track.to_csv('data/one_track.csv', sep='|')
    
    # remove ships that has nan in all eta and ata
    eta_ais = df['eta_ais'].to_numpy().astype(str)
    ata_ais = df['ata_ais'].to_numpy().astype(str)
    nan_eta = eta_ais != 'nan'
    nan_ata = ata_ais != 'nan'
    nan_ata_eta = nan_eta + nan_ata
    
    df = df[nan_ata_eta]
    df = df.set_index(np.arange(df.shape[0]))
    
    # remove multiple status 14 for ships
    status = df['status'].to_numpy()
    a = status != 14
    b = np.roll(a, 1)
    df = df[a+b]
    return df

df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']


df = df.sort_values(by=['track_id'])
track_id = df['track_id'].to_numpy()
number_of_ids = len(np.unique(track_id))

status = df['status'].to_numpy()
arrivals = np.sum(status == 14)

df2 = clean_data(df)

        

# Vi vil i sidste ende gerne kunne regne mean(|eta - ata|)

# parametre vi vil teste

# eta1
# givet et skib og hvor det er på vej hen

# det beregner en rute og givet nogle historiske hastigheder beregnes en eta.

# Givet en log hvor godt rammer vi tidspunktet

# 90 % bedste bud hvor godt rammer vi ata, 

# Hvor godt performer vi for erp_eta.


# eta2
# Containerskibe - kan lave eta på en hele rute

# destination predictor
