"""
This scripts contains functions used in order to obtain the presented results
"""


import pandas as pd
import os
import pickle
import numpy as np


def get_data_eta2():
    """
    Extracts the data from a csv file

    Returns
    -------
    df : pandas dataframe
        Dataframe containing the shipdata.

    """
    
    pardir = os.path.dirname(os.getcwd())
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')
    
    try:
       with open('data/eta2_dataframe.pickle', 'rb') as file:
           df = pickle.load(file)
       print('Pickle loaded')
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe') 
        df = pd.read_csv('data/20210628_eta2_eval_data.csv')
        with open('data/eta2_dataframe.pickle', 'wb') as file:
            pickle.dump(df, file)
        print('Pickling done.')
    return df


def get_data_cleaned_eta2():
    """
    Extracts the data from a csv file

    Returns
    -------
    df : pandas dataframe
        Dataframe containing the cleaned shipdata.

    """
    
    pardir = os.path.dirname(os.getcwd())
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')

    try:
       with open('data/eta2_dataframe_cleaned.pickle', 'rb') as file:
           df = pickle.load(file)
       print('Pickle loaded')
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe') 
        df = pd.read_csv('data/20210628_eta2_eval_data.csv')
        # Adding hours before arrival
        entries = df.entry_id.unique()
        hours_bef_arrive = np.zeros(0)
        for entry in entries:
            df_small = df.loc[df['entry_id']==entry]
            stamp = df_small['timestamp'].to_numpy().astype('datetime64[s]')
            m = len(stamp)
            for i in range(m):
                ata = df_small["ata"].astype('datetime64[s]')
                diff = (ata[:1] - stamp[i]).astype('timedelta64[h]')
                hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
        df['hours_bef_arr'] = hours_bef_arrive
        
        df = df[df["hours_bef_arr"]>=0]
        df = df.reset_index(drop = True)
        with open('data/eta2_dataframe_cleaned.pickle', 'wb') as file:
            pickle.dump(df, file)
        print('Pickling done.')
    return df


def absolute_difference(df):
    """
    Calculates the absolute difference in time of arrivial per hour

    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing the cleaned shipdata.

    Returns
    -------
    mean_eta1 : ndarray
        array containing the mean difference per hour for each city
        for the eta1 algorithm.
    mean_eta2 : ndarray
        array containing the mean difference per hour for each city
        for the eta2 algorithm.
    mean_sta : ndarray
        array containing the mean difference per hour for each city
        for the scheduled arrival.

    """
    
    n = len(df)
    hours = df.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    eta1_err = np.zeros((n,m))
    sta_err = np.zeros((n,m))
    eta2_err = np.zeros((n,m))
    ata = df["ata"].astype('datetime64[s]')
    sta = df["sta"].astype('datetime64[s]')
    eta1 = df["eta1"].astype('datetime64[s]')
    eta2 = df["eta2"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df["hours_bef_arr"][i])
        eta1_err[i, hba] = np.abs(ata[i]-eta1[i]).total_seconds()
        eta2_err[i, hba] = np.abs(ata[i]-eta2[i]).total_seconds()
        sta_err[i, hba] = np.abs(ata[i]-sta[i]).total_seconds()

    mean_eta1 = np.zeros(m)
    mean_eta2 = np.zeros(m)
    mean_sta = np.zeros(m)

    for i in range(m):
        mean_eta1[i] = np.sum(eta1_err[:,i])/np.count_nonzero(eta1_err[:,i])
        mean_eta2[i] = np.sum(eta2_err[:,i])/np.count_nonzero(eta2_err[:,i])
        mean_sta[i] = np.sum(sta_err[:,i])/np.count_nonzero(sta_err[:,i])   
    
    return mean_eta1, mean_eta2, mean_sta


def provider_performance(df, provider):
    """
    Calculates the absolute difference in time of arrival per hour for a
    provider 
    
    Parameters
    ----------
    df : Pandas dataframe
        dataframe containing the shipdata.
    provider : string
        string of a providername.

    Returns
    -------
    mean_eta1 : ndarray
        array of the hourly difference in time of arrival of the eta1
        algorithm.
    mean_eta2 : ndarray
        array of the hourly difference in time of arrival of the eta2
        algorithm.
    mean_sta : ndarray
        array of the hourly difference in time of arrival of the scheduled
        arrival.

    """
    
    df_small = df.loc[df["schedule_source"]== provider]
    df_small = df_small.reset_index(drop = True)
    n = len(df_small)
    hours = df_small.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    eta1_err = np.zeros((n,m))
    sta_err = np.zeros((n,m))
    eta2_err = np.zeros((n,m))
    ata = df_small["ata"].astype('datetime64[s]')
    sta = df_small["sta"].astype('datetime64[s]')
    eta1 = df_small["eta1"].astype('datetime64[s]')
    eta2 = df_small["eta2"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df_small["hours_bef_arr"][i])
        eta1_err[i, hba] = np.abs(ata[i]-eta1[i]).total_seconds()
        eta2_err[i, hba] = np.abs(ata[i]-eta2[i]).total_seconds()
        sta_err[i, hba] = np.abs(ata[i]-sta[i]).total_seconds()

    mean_eta1 = np.zeros(m)
    mean_eta2 = np.zeros(m)
    mean_sta = np.zeros(m)

    for i in range(m):
        mean_eta1[i] = np.sum(eta1_err[:,i])/np.count_nonzero(eta1_err[:,i])
        mean_eta2[i] = np.sum(eta2_err[:,i])/np.count_nonzero(eta2_err[:,i])
        mean_sta[i] = np.sum(sta_err[:,i])/np.count_nonzero(sta_err[:,i])
    return mean_eta1, mean_eta2, mean_sta


def port_performance(df, port):
    """
    Calculates the absolute difference in time of arrival per hour for a
    provider 
    
    Parameters
    ----------
    df : Pandas dataframe
        dataframe containing the shipdata.
    provider : string
        string of a providername.

    Returns
    -------
    mean_eta1 : ndarray
        array of the hourly difference in time of arrival of the eta1
        algorithm.
    mean_eta2 : ndarray
        array of the hourly difference in time of arrival of the eta2
        algorithm.
    mean_sta : ndarray
        array of the hourly difference in time of arrival of the scheduled
        arrival.

    """
    
    df_small = df.loc[df["port"]== port]
    df_small = df_small.reset_index(drop = True)
    n = len(df_small)
    hours = df_small.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    eta1_err = np.zeros((n,m))
    sta_err = np.zeros((n,m))
    eta2_err = np.zeros((n,m))
    ata = df_small["ata"].astype('datetime64[s]')
    sta = df_small["sta"].astype('datetime64[s]')
    eta1 = df_small["eta1"].astype('datetime64[s]')
    eta2 = df_small["eta2"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df_small["hours_bef_arr"][i])
        eta1_err[i, hba] = np.abs(ata[i]-eta1[i]).total_seconds()
        eta2_err[i, hba] = np.abs(ata[i]-eta2[i]).total_seconds()
        sta_err[i, hba] = np.abs(ata[i]-sta[i]).total_seconds()

    mean_eta1 = np.zeros(m)
    mean_eta2 = np.zeros(m)
    mean_sta = np.zeros(m)

    for i in range(m):
        mean_eta1[i] = np.sum(eta1_err[:,i])/np.count_nonzero(eta1_err[:,i])
        mean_eta2[i] = np.sum(eta2_err[:,i])/np.count_nonzero(eta2_err[:,i])
        mean_sta[i] = np.sum(sta_err[:,i])/np.count_nonzero(sta_err[:,i])
    return np.mean(mean_eta1), np.mean(mean_eta2), np.mean(mean_sta)


if __name__ == "__main__":    
    df = get_data_cleaned_eta2()
    providers =  df.schedule_source.unique().tolist()
    sm_mean_eta1, sm_mean_eta2, sm_mean_sta = provider_performance(df, "scraper_maersk")
    