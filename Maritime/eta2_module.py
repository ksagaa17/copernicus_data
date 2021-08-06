"""
This scripts contains functions used in order to obtain the presented results
"""


import pandas as pd
import os
import pickle
import numpy as np
import matplotlib.pyplot as plt


def get_data_eta2(filename):
    """
    Extracts the data from a csv file
    
    Parameters
    ----------
    filename : str
        name of datafile containing the shipdata.
    
    Returns
    -------
    df : pandas dataframe
        Dataframe containing the shipdata.

    """
    
    pardir = os.path.dirname(os.getcwd())
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')
    
    try:
       with open('data/{}_dataframe.pickle'.format(filename), 'rb') as file:
           df = pickle.load(file)
       print('Pickle loaded')
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe') 
        df = pd.read_csv('data/{0}'.format(filename))
        with open('data/{0}_dataframe.pickle'.format(filename), 'wb') as file:
            pickle.dump(df, file)
        print('Pickling done.')
    return df


def get_data_cleaned_eta2(filename):
    """
    Extracts the data from a csv file where entries after arrival has been removed
    and an entry has been added for each hour in areas with no entries.
    
    Parameters
    ----------
    filename : str
        name of datafile containing the shipdata.
    
    Returns
    -------
    df : pandas dataframe
        Dataframe containing the cleaned shipdata.

    """
    
    pardir = os.path.dirname(os.getcwd())
    if not os.path.exists(pardir + '\\Maritime\\data'):
        os.makedirs(pardir + '\\Maritime\\data')

    try:
       with open('data/{0}_dataframe_cleaned.pickle'.format(filename), 'rb') as file:
           df = pickle.load(file)
       print('Pickle loaded')
    
    except FileNotFoundError:
        print('No dataframe pickle found. Pickling dataframe. This takes a while so grab a cup of coffe') 
        df = pd.read_csv('data/{0}'.format(filename))
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
        
        # df_second = pd.DataFrame()
        # for entry in entries:
        #     df_small = df.loc[df["entry_id"]==entry]
        #     n = len(df_small)
        #     df_small = df_small.reset_index(drop=True)
        #     for i in range(2,n):
        #         a = int(df_small["hours_bef_arr"][i-1]-1 - df_small["hours_bef_arr"][i])
        #         if a > 0:
        #             hours = np.zeros(a)
        #             tmp_df = pd.DataFrame()
        #             for j in range(a):
        #                 hours[j] =  df_small["hours_bef_arr"][i-1]-1-j
        #                 df_small.iat[i,9] = hours[j] # Carefull if I ever add another row
        #                 row = df_small.iloc[i] # Carefull if I ever use timestamp again
        #                 df_row = pd.DataFrame(row).transpose()
        #                 tmp_df = tmp_df.append(df_row)
        #             df_second = df_second.append(tmp_df)
        # df2 = df.append(df_second)
        # df2 = df2.sort_values(["entry_id", "hours_bef_arr"], ascending = [True, False])
        # df2 = df2.reset_index(drop=True)
        
        with open('data/{0}_dataframe_cleaned.pickle'.format(filename), 'wb') as file:
            pickle.dump(df, file)
        print('Pickling done.')
    return df


def absolute_difference(df, percent):
    """
    Calculates the absolute difference in time of arrivial per hour

    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing the cleaned shipdata.
        
    percent: float
        percentage of data to be used
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
        place = m-1-hba
        eta1_err[i, place] = np.abs(ata[i]-eta1[i]).total_seconds()
        eta2_err[i, place] = np.abs(ata[i]-eta2[i]).total_seconds()
        sta_err[i, place] = np.abs(ata[i]-sta[i]).total_seconds()

    mean_eta1 = np.zeros(m)
    mean_eta2 = np.zeros(m)
    mean_sta = np.zeros(m)
    
    for i in range(m):
        args = np.where(eta1_err[:,i]!=0)
        eta1_tmp = eta1_err[:,i][args]
        eta2_tmp = eta2_err[:,i][args]
        sta_tmp = sta_err[:,i][args]
        k = len(eta1_tmp)
        if k == 0:
            mean_eta1[i] = mean_eta1[i-1]
            mean_eta2[i] = mean_eta2[i-1]
            mean_sta[i] = mean_sta[i-1]
        else:
            length = int(np.ceil(k*percent))
            eta1_use = np.sort(eta1_tmp)[:length]
            eta2_use = np.sort(eta2_tmp)[:length]
            sta_use = np.sort(sta_tmp)[:length]
            mean_eta1[i] = np.sum(eta1_use)/length
            mean_eta2[i] = np.sum(eta2_use)/length
            mean_sta[i] = np.sum(sta_use)/length   
    
    return mean_eta1, mean_eta2, mean_sta




def absolute_difference_eta1(df, percent):
    """
    Calculates the absolute difference in time of arrivial per hour

    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing the cleaned shipdata.
        
    percent: float
        percentage of data to be used
    Returns
    -------
    mean_eta1 : ndarray
        array containing the mean difference per hour for each city
        for the eta1 algorithm.

    """
    
    n = len(df)
    hours = df.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    eta1_err = np.zeros((n,m))
    ata = df["ata"].astype('datetime64[s]')
    eta1 = df["eta1"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df["hours_bef_arr"][i])
        place = m -1 -hba
        eta1_err[i, place] = np.abs(ata[i]-eta1[i]).total_seconds()

    mean_eta1 = np.zeros(m)

    for i in range(m):
        args = np.where(eta1_err[:,i]!=0)
        eta1_tmp = eta1_err[:,i][args]
        k = len(eta1_tmp)
        if k == 0:
            mean_eta1[i] = mean_eta1[i-1]
        else:
            length = int(np.ceil(k*percent))
            eta1_use = np.sort(eta1_tmp)[:length]
            mean_eta1[i] = np.sum(eta1_use)/length
    
    return mean_eta1


def absolute_difference_eta2(df, percent):
    """
    Calculates the absolute difference in time of arrivial per hour

    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing the cleaned shipdata.
        
    percent: float
        percentage of data to be used
    Returns
    -------
    mean_eta2 : ndarray
        array containing the mean difference per hour for each city
        for the eta2 algorithm.

    """
    
    n = len(df)
    hours = df.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    eta2_err = np.zeros((n,m))
    ata = df["ata"].astype('datetime64[s]')
    eta2 = df["eta2"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df["hours_bef_arr"][i])
        place = m-1-hba
        eta2_err[i, place] = np.abs(ata[i]-eta2[i]).total_seconds()

    mean_eta2 = np.zeros(m)

    for i in range(m):
        args = np.where(eta2_err[:,i]!=0)
        eta2_tmp = eta2_err[:,i][args]
        k = len(eta2_tmp)
        if k == 0:
            mean_eta2[i]= mean_eta2[i-1]
        else:
            length = int(np.ceil(k*percent))
            eta2_use = np.sort(eta2_tmp)[:length]
            mean_eta2[i] = np.sum(eta2_use)/length  
    
    return mean_eta2


def absolute_difference_sta(df, percent):
    """
    Calculates the absolute difference in time of arrivial per hour

    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing the cleaned shipdata.
        
    percent: float
        percentage of data to be used
    Returns
    -------
    mean_sta : ndarray
        array containing the mean difference per hour for each city
        for the scheduled arrival.

    """
    
    n = len(df)
    hours = df.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    sta_err = np.zeros((n,m))
    ata = df["ata"].astype('datetime64[s]')
    sta = df["sta"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df["hours_bef_arr"][i])
        place = m-1-hba
        sta_err[i, place] = np.abs(ata[i]-sta[i]).total_seconds()

    mean_sta = np.zeros(m)

    for i in range(m):
        args = np.where(sta_err[:,i]!=0)
        sta_tmp = sta_err[:,i][args]
        k = len(sta_tmp)
        if k == 0:
            mean_sta[i]=mean_sta[i-1]
        else:
            length = int(np.ceil(k*percent))
            sta_use = np.sort(sta_tmp)[:length]
            mean_sta[i] = np.sum(sta_use)/length   
    
    return mean_sta


def absolute_difference_nextport(df, percent):
    """
    Calculates the absolute difference in time of arrivial per hour

    Parameters
    ----------
    df : Pandas dataframe
        Dataframe containing the cleaned shipdata.
        
    percent: float
        percentage of data to be used
    Returns
    -------
    mean_sta : ndarray
        array containing the mean difference per hour for each city
        for the nextport.

    """
    
    nextport = df['nextport_eta'].to_numpy().astype(str)
    nan_nextport = nextport != 'nan'
    df_small = df[nan_nextport]
    df_small = df_small.reset_index(drop = True)
    
    n = len(df_small)
    hours = df_small.hours_bef_arr.unique().tolist()
    m = int(np.max(hours))+1
    nport_err = np.zeros((n,m))
    ata = df_small["ata"].astype('datetime64[s]')
    nport = df_small["nextport_eta"].astype('datetime64[s]')

    for i in range(n):
        hba = int(df_small["hours_bef_arr"][i])
        place = m - 1 - hba
        nport_err[i, place] = np.abs(ata[i]-nport[i]).total_seconds()

    mean_nport = np.zeros(m)

    for i in range(m):
        args = np.where(nport_err[:,i]!=0)
        nport_tmp = nport_err[:,i][args]
        k = len(nport_tmp)
        if k==0:
            mean_nport[i] = mean_nport[i-1]
        else:
            length = int(np.ceil(k*percent))
            nport_use = np.sort(nport_tmp)[:length]
            mean_nport[i] = np.sum(nport_use)/length   
    
    return mean_nport


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
    return mean_eta1, mean_eta2, mean_sta


def attribute_plot(mean_eta1, mean_eta2, mean_schedule, plttitle, zoom):
    """
    makes a plot showcasing the performance of a given attribute
    
    Parameters
    ----------
    mean_eta1 : ndarray
        contains the mean eta1 error for each hour away from destination
    mean_eta2 : ndarray
        contains the mean eta2 error for each hour away from destination.
    mean_schedule : ndarray
        contains the mean schedule error for each hour away from destination..
    plttitle : str
        title of plot.
    zoom : int
        zoom of plot.

    Returns
    -------
    A plot and saves the figure using zoom and plttitle.

    """
    n = len(mean_eta1)
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()
    xticks = np.linspace(1,n,n)
    ax.plot(xticks, mean_eta1/(60*60))
    ax.plot(xticks, mean_eta2/(60*60))
    ax.plot(xticks, mean_schedule/(60*60))
    ax.invert_xaxis()
    ax.set_ylabel("Absolute error in hours")
    ax.set_xlabel('Hours before arrival')
    plt.legend(["eta1","eta2", "schedule"])
    plt.title("{0}".format(plttitle))
    plt.savefig("figures/{0}_{1}.pdf".format(plttitle, zoom))
    plt.show()
    



def plot_entry(df, entry_id):
    """
    makes a plot showing the data for an entry id
    
    Parameters
    ----------
    df : Pandas dataframe
        ship arrival data.
    entry_id : int
        entry_id of a ship.

    Returns
    -------
    a plot and saves the figure

    """
    
    df_small = df.loc[df["entry_id"] == entry_id]
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
    
    habour = df_small["port"][0]
    provider = df_small["schedule_source"][0]
    
    k = len(mean_eta1)
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()
    xticks = np.linspace(1,k,k)
    ax.plot(xticks, mean_eta1/(60*60))
    ax.plot(xticks, mean_eta2/(60*60))
    ax.plot(xticks, mean_sta/(60*60))
    ax.invert_xaxis()
    ax.set_ylabel("Absolute error in hours")
    ax.set_xlabel('Hours before arrival')
    plt.legend(["eta1","eta2", "schedule"])
    plt.title("{0}_{1}_{2}".format(entry_id, habour, provider))
    plt.savefig("figures/{0}_{1}_{2}.pdf".format(entry_id, habour, provider))
    plt.show()


if __name__ == "__main__":    
    file = "eta2_dump.csv"
    df = get_data_cleaned_eta2(file)
    #percent = 0.9
    #nport = absolute_difference_nextport(df, percent)
    #mean1, mean2, means = absolute_difference(df, percent)
    # providers =  df.schedule_source.unique().tolist()
    # sm_mean_eta1, sm_mean_eta2, sm_mean_sta = provider_performance(df, "scraper_maersk")
    # test add entries
    # entries =  df.entry_id.unique().tolist()
    # df_second = pd.DataFrame()
    # for entry in entries:
    #     df_small = df.loc[df["entry_id"]==entry]
    #     n = len(df_small)
    #     df_small = df_small.reset_index(drop=True)
    #     for i in range(2,n):
    #         a = int(df_small["hours_bef_arr"][i-1]-1 - df_small["hours_bef_arr"][i])
    #         if a > 0:
    #             hours = np.zeros(a)
    #             tmp_df = pd.DataFrame()
    #             for j in range(a):
    #                 hours[j] =  df_small["hours_bef_arr"][i-1]-1-j
    #                 df_small.iat[i,9] = hours[j] # Carefull if I ever add another row
    #                 row = df_small.iloc[i] # Carefull if I ever use timestamp again
    #                 df_row = pd.DataFrame(row).transpose()
    #                 tmp_df = tmp_df.append(df_row)
    #             df_second = df_second.append(tmp_df)
    # df2 = df.append(df_second)
    # df2 = df2.sort_values(["entry_id", "hours_bef_arr"], ascending = [True, False])
    # df2 = df2.reset_index(drop=True)
