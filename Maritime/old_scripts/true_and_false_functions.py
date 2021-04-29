# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 19:46:17 2021

@author: krist
"""

import pandas as pd
import numpy as np
import utillities as ut

def add_hours_bef_arr(df):
    """
    Add column with hours before arrival based on the time stamp.

    Parameters
    ----------
    df : pandas dataframe
        cleaned Log fra ETA1.

    Returns
    -------
    df : pandas dataframe
        Log fra ETA1 with additional column with  hours before arrival.

    """
    track_ids = df.track_id.unique()
    hours_bef_arrive = np.zeros(0)
    for track_id in track_ids:
        df_small = df.loc[df['track_id']==track_id]
        stamp = df_small['stamp'].to_numpy().astype('datetime64[s]')
        ata = ut.ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
        diff = (ata - stamp).astype('timedelta64[h]')
        hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
    
    df['hours_bef_arr'] = hours_bef_arrive
    return df


def erp_is_nan(df):
    """
    Add boolean column indicating whether eta_erp is nan or not. 

    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.

    Returns
    -------
    df : pandas dataframe
        Log fra ETA1 with additional column indicating whether eta_erp is nan or not.

    """
    erp = df['eta_erp'].to_numpy().astype(str)
    erp_is_nan = erp == 'nan'

    df['erp_is_nan'] = erp_is_nan
    return df


def erp_before_ata(df):
    """
    Add boolean column indicating whether eta_erp <= ata_ais for each track_id.
    
    NOTE if eta_erp == nan, we will put False in the erp_bef_ata column.

    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.

    Returns
    -------
    df : pandas dataframe
        Log fra ETA1 with additional column indicating whether eta_erp <= ata_ais.

    """
    if any(df.columns != 'erp_is_nan'):
        df = erp_is_nan(df)
    
    track_ids = df.track_id.unique()
    erp_bef_ata = np.empty(0, dtype=bool)
    for track_id in track_ids:
        df_small = df.loc[df['track_id']==track_id]
        if any(df_small['erp_is_nan'] == True):
            erp_bef_ata = np.concatenate((erp_bef_ata, np.zeros(df_small.shape[0], dtype=bool)))
        else:
            ata = ut.ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
            erp = df_small['eta_erp'].to_numpy().astype('datetime64[s]')
            erp_bef_ata_id = erp <= ata
            erp_bef_ata = np.concatenate((erp_bef_ata, erp_bef_ata_id))

    df['erp_bef_ata'] = erp_bef_ata
    return df


def ais_before_erp(df):
    """
    Add column indicating whether eta_ais <= eta_erp. If eta_erp == nan we return True.
    If eta_ais == nan we return False. 

    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.

    Returns
    -------
    df : pandas dataframe
        Log fra ETA1 with additional column indicating whether eta_ais <= eta_erp.

    """
    track_ids = df.track_id.unique()
    
    ais_bef_erp = np.empty(0, dtype=bool)
    for track_id in track_ids:
        df_small = df.loc[df['track_id']==track_id]
        ais = df_small['eta_ais'].to_numpy().astype(str)
        erp = df_small['eta_erp'].to_numpy().astype(str)
        ais_bef_erp_id = np.empty(df_small.shape[0], dtype=bool)
        for i in range(len(ais)):
            if ais[i] == 'nan':
                ais_bef_erp_id[i] = False
            elif erp[i] == 'nan':
                ais_bef_erp_id[i] = True
            elif erp[i].astype('datetime64[s]') >= ais[i].astype('datetime64[s]'):
                ais_bef_erp_id[i] = True
            else:
                ais_bef_erp_id[i] = False
                
        ais_bef_erp = np.concatenate((ais_bef_erp, ais_bef_erp_id))
            
    df['ais_bef_erp'] = ais_bef_erp
    return df


def data_prepocessing(df):
    """
    Collection of the functionality of 
    - add_hours_bef_arr()
    - erp_is_nan()
    - erp_before_ata()
    - ais_before_erp()

    Parameters
    ----------
    df :  pandas dataframe
        Log fra ETA1.

    Returns
    -------
    df :  pandas dataframe
         Log fra ETA1 with additional columns.

    """
    
    # Add erp is nan column
    erp = df['eta_erp'].to_numpy().astype(str)
    erp_is_nan = erp == 'nan'
    df['erp_is_nan'] = erp_is_nan
    
    
    track_ids = df.track_id.unique()
    hours_bef_arrive = np.zeros(0)
    erp_bef_ata = np.empty(0, dtype=bool)
    ais_bef_erp = np.empty(0, dtype=bool)
    
    for track_id in track_ids:
        # Add hours before arrival column
        df_small = df.loc[df['track_id']==track_id]
        stamp = df_small['stamp'].to_numpy().astype('datetime64[s]')
        ata = ut.ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
        diff = (ata - stamp).astype('timedelta64[h]')
        hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
        
        # Add erp before ata column
        if any(df_small['erp_is_nan'] == True):
            erp_bef_ata = np.concatenate((erp_bef_ata, np.zeros(df_small.shape[0], dtype=bool)))
        else:
            erp = df_small['eta_erp'].to_numpy().astype('datetime64[s]')
            erp_bef_ata_id = erp <= ata
            erp_bef_ata = np.concatenate((erp_bef_ata, erp_bef_ata_id))
        
        # Add ais before erp column
        ais = df_small['eta_ais'].to_numpy().astype(str)
        erp = df_small['eta_erp'].to_numpy().astype(str)
        ais_bef_erp_id = np.empty(df_small.shape[0], dtype=bool)
        for i in range(len(ais)):
            if ais[i] == 'nan':
                ais_bef_erp_id[i] = False
            elif erp[i] == 'nan':
                ais_bef_erp_id[i] = True
            elif erp[i].astype('datetime64[s]') >= ais[i].astype('datetime64[s]'):
                ais_bef_erp_id[i] = True
            else:
                ais_bef_erp_id[i] = False
                
        ais_bef_erp = np.concatenate((ais_bef_erp, ais_bef_erp_id))
            
    
    
    df['hours_bef_arr'] = hours_bef_arrive
    df['erp_bef_ata'] = erp_bef_ata
    df['ais_bef_erp'] = ais_bef_erp
    return df


if __name__ == "__main__":
    import time

    t1 = time.time()    
    df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                  'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    t2 = time.time()
    print("Load time: {}".format(t2-t1))
    print("")
    
    
    df = ut.clean_data(df)
    
    t3 = time.time()
    
    df1= erp_is_nan(df)
    df1 = erp_before_ata(df1)
    df1 = ais_before_erp(df1)
    
    t4 = time.time()
    print(t4-t3)
    
    df2 = data_prepocessing(df)
    t5 = time.time()
    print(t5-t4)
    