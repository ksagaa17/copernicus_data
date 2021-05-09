from datetime import datetime
import numpy as np
import os
import pickle
import pandas as pd

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
    return abs(sek_diff)


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
        diff = (ata[:1] - stamp).astype('timedelta64[h]')
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
            ata = ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
            erp = df_small['eta_erp'].to_numpy().astype('datetime64[s]')
            erp_bef_ata_id = erp <= ata[:1]
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


def add_eta_error(df):
    """
    Add columns with the absolute difference between eta_erp and ata_ais and 
    between eta_ais and ata_ais. The difference is given in seconds.

    Parameters
    ----------
    df :pandas dataframe
        Log fra ETA1.

    Returns
    -------
    df :  pandas dataframe
         Log fra ETA1 with additional columns of eta errors.

    """
    track_ids = df.track_id.unique()
    n = len(track_ids)
    
    
    ais_diff_list = np.zeros(0)
    erp_diff_list = np.zeros(0)
    
    for i in range(n):
        ata = ata_Extract(df, track_ids[i]).astype('datetime64[s]')
        
        df_small = df[df["track_id"]==track_ids[i]]
        ais = df_small["eta_ais"].to_numpy().astype(str)
        idx = ais != 'nan'
        ais_diff = np.ones(len(ais))*np.nan
        ais_diff[idx] = np.abs(ata[:1] - ais[idx].astype('datetime64[s]'))
        ais_diff_list = np.concatenate((ais_diff_list, ais_diff))
        
        erp = df_small["eta_erp"].to_numpy().astype(str)
        idx = erp != 'nan'
        erp_diff = np.ones(len(ais))*np.nan
        erp_diff[idx] = np.abs(ata[:1] - erp[idx].astype('datetime64[s]'))
        erp_diff_list = np.concatenate((erp_diff_list, erp_diff))
        
        
    df['erp_error'] = erp_diff_list
    df['ais_error'] = ais_diff_list
    
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
        ata = ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
        diff = (ata[:1] - stamp).astype('timedelta64[h]')
        hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
        
        # Add erp before ata column
        if any(df_small['erp_is_nan'] == True):
            erp_bef_ata = np.concatenate((erp_bef_ata, np.zeros(df_small.shape[0], dtype=bool)))
        else:
            erp = df_small['eta_erp'].to_numpy().astype('datetime64[s]')
            erp_bef_ata_id = erp <= ata[:1]
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


def Extract_time_brackets(df, time_low, time_high, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time frame and track_id
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    time_low : int
        time before arrival lower bound
    time_high : int
        time before arrival upper bound
    track_id : int
        A track_id from df.

    Returns
    -------
    eta_erp : ndarray
        eta_erp for the given track_id.
    eta_ais : ndarray
        eta_ais for the given track_id.
    """
    
    indexes = df.query('hours_bef_arr >= {0} & hours_bef_arr < {1} & track_id == {2}'.format(time_low, time_high, track_id)).index
    eta_erp = df['eta_erp'][indexes]
    eta_ais = df['eta_ais'][indexes]
    
    eta_erp = eta_erp.astype(str).to_numpy()
    eta_ais = eta_ais.astype(str).to_numpy()
    
    eta_erp = eta_erp[eta_erp != 'nan']
    eta_ais = eta_ais[eta_ais != 'nan']
    return eta_erp, eta_ais


def max_hour(df, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time frame and track_id
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    track_id : int
        A track_id from df.

    Returns
    -------
    max_hour : int
        maximum hour before arrvival.
    """
    
    indexes = df.query('track_id == {0}'.format(track_id)).index
    hours_before = df['hours_bef_arr'][indexes]
    max_hours = hours_before.max()
    return max_hours


def Extract_ais_specific(df, time_low, time_high, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time frame and track_id
    Parameters
    ----------
    df : pandas dataframe with added hours bef arr
        Log fra ETA1.
    time_low : int
        time before arrival lower bound
    time_high : int
        time before arrival upper bound
    track_id : int
        A track_id from df.

    Returns
    -------
    eta_ais : ndarray
        eta_ais for the given track_id.
    """
    
    indexes = df.query('hours_bef_arr >= {0} & hours_bef_arr < {1} & track_id == {2} & erp_bef_ata == True & ais_bef_erp == False'.format(time_low, time_high, track_id)).index
    eta_ais = df['eta_ais'][indexes]
    
    eta_ais = eta_ais.astype(str).to_numpy()
    
    eta_ais = eta_ais[eta_ais != 'nan']
    return eta_ais


def Extract_time_brackets_erp(df, time_low, time_high, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time frame and track_id
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    time_low : int
        time before arrival lower bound
    time_high : int
        time before arrival upper bound
    track_id : int
        A track_id from df.

    Returns
    -------
    eta_erp : ndarray
        eta_erp for the given track_id.
    """
    
    indexes = df.query('hours_bef_arr >= {0} & hours_bef_arr < {1} & track_id == {2}'.format(time_low, time_high, track_id)).index
    eta_erp = df['eta_erp'][indexes]
    
    eta_erp = eta_erp.astype(str).to_numpy()
    
    eta_erp = eta_erp[eta_erp != 'nan']
    return eta_erp


def Extract_time_brackets_all_tracks(df, time_low, time_high):
    """
    Extracts the erp_error and ais_error at a given time frame
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    time_low : int
        time before arrival lower bound
    time_high : int
        time before arrival upper bound


    Returns
    -------
    erp_err : ndarray
        erp_error for the given time frame.
    eta_ais : ndarray
        ais_error for the given time frame.
    """
    
    indexes = df.query('hours_bef_arr >= {0} & hours_bef_arr < {1}'.format(time_low, time_high)).index
    erp_err = df['erp_error'][indexes]
    ais_err = df['ais_error'][indexes]
    
    erp_err = erp_err.to_numpy().astype(str)
    ais_err = ais_err.to_numpy().astype(str)
    
    erp_err = erp_err[erp_err != 'nan']
    ais_err = ais_err[ais_err != 'nan']
    return erp_err, ais_err


def get_data(month):
    """
    Read data from txt

    Parameters
    ----------
    month : int 
        the month of interest
        MM.
    Returns
    -------
    df : pandas datframe
        ship eta data.
    """
    pardir = os.path.dirname(os.getcwd())
    supported_months = [1, 2, 3]
    if month not in supported_months:
        raise ValueError("This month is not currently supported. Supported months are {}".format(supported_months))
    
    # Make folder for dataframes if not found
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')
    try:
        with open(f'./data/{month:02d}_dataframe.pickle', 'rb') as file:
            df = pickle.load(file)
        print('Pickle loaded')
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe') 
        df = pd.read_csv(f'./data/tbl_ship_arrivals_log_2021{month:02d}.log', sep = "|", header=None)
        df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                      'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    
        with open(f'./data/{month:02d}_dataframe.pickle', 'wb') as file:
                pickle.dump(df, file)
        
        print('Pickling done.')
    return df


def get_data_cleaned(month):
    """
    Read data from txt

    Parameters
    ----------
    month : int 
        the month of interest
        MM.
    Returns
    -------
    df : pandas datframe
        ship eta data.
    """
    pardir = os.path.dirname(os.getcwd())
    supported_months = [1, 2, 3]
    if month not in supported_months:
        raise ValueError("This month is not currently supported. Supported months are {}".format(supported_months))
    
    # Make folder for dataframes if not found
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')
    try:
        with open(f'./data/{month:02d}_cleaned_dataframe.pickle', 'rb') as file:
            df = pickle.load(file)
        print('Pickle loaded')
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe') 
        df = pd.read_csv(f'./data/tbl_ship_arrivals_log_2021{month:02d}.log', sep = "|", header=None)
        df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                      'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
        df = clean_data(df)
        df = add_hours_bef_arr(df)
        df = erp_before_ata(df) 
        df = ais_before_erp(df) 
        df = add_eta_error(df)
    
        with open(f'./data/{month:02d}_cleaned_dataframe.pickle', 'wb') as file:
                pickle.dump(df, file)
        
        print('Pickling done.')
    return df


def get_data_all_month():
    pardir = os.path.dirname(os.getcwd())

    # Make folder for dataframes if not found
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')
    try:
        with open(f'./data/all_months_dataframe.pickle', 'rb') as file:
            df = pickle.load(file)
        print('Pickle loaded')
    
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe')
        supported_months = [1, 2, 3]
        month = 1
        df = pd.read_csv(f'./data/tbl_ship_arrivals_log_2021{month:02d}.log', sep = "|", header=None)
        df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                      'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
        for month in supported_months:
            df1 = pd.read_csv(f'./data/tbl_ship_arrivals_log_2021{month:02d}.log', sep = "|", header=None)
            df1.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                      'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
            df = pd.concat([df, df1])
    
        with open(f'./data/all_months_dataframe.pickle', 'wb') as file:
                pickle.dump(df, file)
        
        print('Pickling done.')
    return df


def get_data_all_month_cleaned():
    pardir = os.path.dirname(os.getcwd())

    # Make folder for dataframes if not found
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')
    try:
        with open(f'./data/all_months_cleaned_dataframe.pickle', 'rb') as file:
            df = pickle.load(file)
        print('Pickle loaded')
    
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe')
        supported_months = [1, 2, 3]
        month = 1
        df = pd.read_csv(f'./data/tbl_ship_arrivals_log_2021{month:02d}.log', sep = "|", header=None)
        df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                      'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
        for month in supported_months:
            df1 = pd.read_csv(f'./data/tbl_ship_arrivals_log_2021{month:02d}.log', sep = "|", header=None)
            df1.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                      'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
            
            df = pd.concat([df, df1])
            
        df = clean_data(df)
        df = add_hours_bef_arr(df)
        df = erp_before_ata(df) # Only nessescary when used for filters
        df = ais_before_erp(df) # Only nessescary when used for filters
        df = add_eta_error(df)
        
        with open(f'./data/all_months_cleaned_dataframe.pickle', 'wb') as file:
                pickle.dump(df, file)
        
        print('Pickling done.')
    return df

if __name__ == "__main__":    
    # df = get_data(3)
    # df_cleaned = get_data_cleaned(3)
    df = get_data_all_month_cleaned()
