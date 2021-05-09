# -*- coding: utf-8 -*-
"""
Created on Sun May  2 12:30:25 2021

@author: krist
"""

import utillities as ut
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# =============================================================================
# VÆR OPMÆRKSOM PÅ FILTRERING - GØR DEN SOM VI ØNSKER
# =============================================================================    


def relative_error(df, filters, bracketwidth = 5, percent = 0.9):
    """
    Computes the relative mean absolute error for eta_erp and eta_ais based
    on data in 'df' filtered by the 'filters'. 

    Parameters
    ----------
    df : pandas dataframe
        Cleaned and augmented log fra ETA1. The dataframe should at least contain
        columns used in filters and the erp_error and ais_error.
    filters : dictionary
        Specifying what data we use.
    bracketwidth : int, optional
        How many hours we use in each group. The default is 5.
    percent : float, optional
        Specifies the how much data used in each group. Must be between 0 and 1. 
        The default is 0.9.

    Returns
    -------
    mean_erp : ndarray
        The relative mean absolute error in each timebracket for erp.
    mean_ais : ndarray
        The relative mean absolute error in each timebracket for ais.

    """
    
    # Use filters
    df_filter = df
    for key in filters.keys():
        df_filter = df_filter[df_filter[key] == filters[key]]
    
    
    track_ids = df_filter.track_id.unique()
    n = len(track_ids)
    
    # Determining the maximum amount of hours away we have data for
    max_hours = np.zeros(n)
    for i in range(n):
        max_hours[i] = ut.max_hour(df_filter, track_ids[i])
    
    # Maximum amount of points
    points = int(np.ceil(np.max(max_hours)/bracketwidth) + 1) 
    mean_erp = np.zeros(points)
    mean_ais = np.zeros(points)
    
    ### compute relative mean absolute error ###
    time_low = 0
    time_high = bracketwidth
    for i in range(points):
        erp_error, ais_error = ut.Extract_time_brackets_all_tracks(df_filter, time_low, time_high)
        divisor = 1/((time_low + time_high)*3600/2) # in each bracket we divide by the mean of that bracket
        
        erp_error = erp_error.astype(float)
        ais_error = ais_error.astype(float)
        
        mean_erp[i] = np.mean(erp_error*divisor)
        
        ais_length = int(len(ais_error)*percent) 
        print(ais_length)
        ais_error = np.sort(ais_error)[:ais_length] # use only the percent best 
        mean_ais[i] = np.mean(ais_error*divisor)
        
        time_low += bracketwidth
        time_high += bracketwidth
    
    return mean_erp, mean_ais


def plot_relative_error(df, filters, month, bracketwidth = 5, percent = 0.9, returns = True):
    """
    Plots the relative mean absolute error for the eta_erp and eta_ais. 


    Parameters
    ----------
    df : pandas dataframe
        Cleaned and augmented log fra ETA1. The dataframe should at least contain
        columns used in filters and the erp_error and ais_error.
    filters : dictionary
        Specifying what data we use.
    month : int or str
        Specifies which month is used in the data. Only used in figname.
    bracketwidth : int, optional
        How many hours we use in each group. The default is 5.
    percent : float, optional
        Specifies the how much data used in each group. Must be between 0 and 1. 
        The default is 0.9.
    returns : bool, optional
        Whether or not to return the mean_erp and mean_ais. The default is True.

    Returns
    -------
    mean_erp : ndarray
        The relative mean absolute error in each timebracket for erp.
    mean_ais : ndarray
        The relative mean absolute error in each timebracket for ais.

    """
    mean_erp, mean_ais = relative_error(df, filters, bracketwidth = bracketwidth, percent = percent)
    fig_filter = ""
    for key in filters.keys():
        if filters[key] == True:
            fig_filter = fig_filter + key + "T_"
        else:
            fig_filter = fig_filter + key + "F_"
        
    x_ticks = []
    for i in range(len(mean_ais)):
         a = i*bracketwidth
         tic = "{}-{}".format(a, a + bracketwidth)
         x_ticks.append(tic)
    
    ten_percent = 0.1*np.ones(len(x_ticks))
    
    plt.style.use('seaborn-darkgrid')
    fig, ax = plt.subplots()
    if any(mean_erp.astype(str) != 'nan'):
        ax.plot(x_ticks, mean_erp, label='eta_erp')
    ax.plot(x_ticks, mean_ais, label='eta_ais', color='tab:orange')
    ax.plot(x_ticks, ten_percent, color='r', linestyle = 'dashed')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
    ax.invert_xaxis()
    ax.set_ylabel("Relative mean absolute error")
    ax.set_xlabel('Hours before arrival')
    plt.legend()
    plt.savefig("figures/relative/relative_err_{0}_bw{1}_{2}_{3}".format(fig_filter, bracketwidth, int(100*percent), month))
    plt.show()
    
    if returns == True:
        return mean_erp, mean_ais

if __name__ == "__main__":
    # Load and clean data
    month = 'all'
    df = ut.get_data_all_month_cleaned()

    # settings for  
    bracketwidth = 5
    percent = 0.9
    
    #my_filters = {'erp_bef_ata': True, 'ais_bef_erp': False}
    my_filters = {'erp_is_nan': True}
    mean_erp, mean_ais = plot_relative_error(df, my_filters, month, 
                                             bracketwidth = bracketwidth, 
                                             percent = percent)
    
    
