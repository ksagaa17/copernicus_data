# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 17:46:20 2021

@author: krist
"""

import pandas as pd
from datetime import datetime
import numpy as np

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
    # remove rows with status 16
    df = df[df['status'] != 16]
    
    # remove ships that has not arrived
    df_arrive = df[df['status'] == 14]
    df = df[df['track_id'].isin(df_arrive['track_id'])]
    
    # remove ships that only has status 14 in the log
    df_eta = df[df['status'] != 14]
    df = df[df['track_id'].isin(df_eta['track_id'])]
    df = df.sort_values(by=['track_id', 'stamp'])
    
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


def TimeDifference(time_1,time_2):
    """
    Calculates absolute time difference between two timestamps in the 
    YYYY-mm-dd HH:MM:SS format.
    Parameters
    ----------
    time_1 : str
        first timestamp.
    time_2: str
        second timestamp.

    Returns
    -------
    sek_diff : int 
        absolute time difference between time_1 and time_2.
    """
    
    FMT = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(time_1, FMT) - datetime.strptime(time_2, FMT)
    sek_diff = tdelta.days * 24 * 3600 + tdelta.seconds
    return sek_diff


def Day_trackid(df, track_id):
    """
    Extracts days for a given track_id of a dataframe
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    track_id: int
        A track_id from df

    Returns
    -------
    days : ndarray 
        days related to the track_id.
    """
    
    indexes = df.query('track_id == {0}'.format(track_id)).index
    days = df['day'][indexes]
    days = days.unique()  
    return days


def Hour_trackid(df, track_id, day):
    """
    Extracts hours for a given track_id and day of a dataframe
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    track_id: int
        A track_id from df
    day: int
        A day for which track_id has data

    Returns
    -------
    hours : ndarray 
        hours related to the track_id for the given day.
    """
    
    indexes = df.query('track_id == {0} & day == {1}'.format(track_id, day)).index
    hours = df['hour'][indexes] 
    hours = hours.unique()    
    return hours


def ata_Extract(df, track_id, status = 14):
     """
    Extracts the ata_ais for a given track_id for a dataframe
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    track_id: int
        A track_id from df

    Returns
    -------
    ata_ais : ndarray 
        ata_ais for the given track_id.
     """
     
     indexes = df.query('track_id == {0} & status == {1}'.format(track_id, status)).index
     ata_ais = df['ata_ais'][indexes]
     ata_ais = ata_ais.unique().astype(str)
     ata_ais = ata_ais[ata_ais != 'nan']
     return ata_ais


def eta_Extract(df, hour, day, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time and track_id for a dataframe
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    hour : int
        An hour containing data from the track_id
    day : int
        A day containing data from the track_id
    track_id : int
        A track_id from df.

    Returns
    -------
    eta_erp : ndarray
        eta_erp for the given track_id.
    eta_ais : ndarray
        eta_ais for the given track_id.
    """
    
    indexes = df.query('hour == {0} & day == {1} & track_id == {2}'.format(hour, day, track_id)).index
    eta_erp = df['eta_erp'][indexes]
    eta_ais = df['eta_ais'][indexes]
    
    eta_erp = eta_erp.unique().astype(str)
    eta_ais = eta_ais.unique().astype(str)
    
    eta_erp = eta_erp[eta_erp != 'nan']
    eta_ais = eta_ais[eta_ais != 'nan']
    return eta_erp, eta_ais


def eta_Extract_whole_track(df, track_id):
    """
    Extracts the eta_erp and eta_ais for a given track_id for a dataframe. 
    Returns these in numpy arrays.

    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    track_id : int
        A track_id from df.

    Returns
    -------
    eta_erp : ndarray
        eta_erp for the given track_id.
    eta_ais : ndarray
        eta_ais for the given track_id.
    """
    
    indexes = df.query('track_id == {0}'.format(track_id)).index
    eta_erp = df['eta_erp'][indexes]
    eta_ais = df['eta_ais'][indexes]
    
    eta_erp = eta_erp.unique().astype(str)
    eta_ais = eta_ais.unique().astype(str)
    
    eta_erp = eta_erp[eta_erp != 'nan']
    eta_ais = eta_ais[eta_ais != 'nan']
    return eta_erp, eta_ais

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
        ata = ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
        diff = (ata - stamp).astype('timedelta64[h]')
        hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
    
    df['hours_bef_arr'] = hours_bef_arrive
    return df