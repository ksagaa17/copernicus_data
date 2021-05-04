# -*- coding: utf-8 -*-
"""
Created on Sun May  2 12:30:25 2021

@author: krist
"""

import utillities as ut
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# =============================================================================
# VÆR OPMÆRKSOM PÅ FILTRERING - GØR DEN SOM VI ØNSKER
# =============================================================================    


def relative_error(df, filters, bracketwidth = 5, percent = 0.9):
    
    # filters = {'erp_bef_ata': False}
    
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
    
    ### ais hourly percentage ###
    time_low = 0
    time_high = bracketwidth
    for i in range(points):
        erp_error, ais_error = Extract_time_brackets_all_tracks(df_filter, time_low, time_high)
        divisor = 1/((time_low + time_high)*3600/2)
        
        erp_error = erp_error.astype(float)
        ais_error = ais_error.astype(float)
        
        mean_erp[i] = np.mean(erp_error*divisor)
        
        ais_length = int(len(ais_error)*percent)
        print(ais_length)
        ais_error = np.sort(ais_error)[:ais_length]
        mean_ais[i] = np.mean(ais_error*divisor)
        
        time_low += bracketwidth
        time_high += bracketwidth
    
    return mean_erp, mean_ais


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


def plot_relative_error(figname, df, filters, bracketwidth = 5, percent = 0.9, zoom = None, returns = True):
    mean_erp, mean_ais = relative_error(df, filters, bracketwidth = bracketwidth, percent = percent)
    x_ticks = []
    for i in range(len(mean_ais)):
         a = i*bracketwidth
         tic = "{}-{}".format(a, a + bracketwidth)
         x_ticks.append(tic)
    
    if zoom == None:
        zoom = [0, len(mean_ais)]
    #time = np.linspace(0, np.max(max_hours), points)
    fig, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')
    ax.plot(x_ticks[zoom[0]:zoom[1]], mean_erp[zoom[0]:zoom[1]], label='eta_erp')
    ax.plot(x_ticks[zoom[0]:zoom[1]], mean_ais[zoom[0]:zoom[1]], label='eta_ais')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
    ax.invert_xaxis()
    ax.set_ylabel("Relative mean absolute error")
    ax.set_xlabel('Hours before arrival')
    plt.legend()
    plt.savefig("figures/relative/"+ figname + "{0}_{1}".format(int(100*percent), zoom))
    plt.show()
    
    if returns == True:
        return mean_erp, mean_ais

if __name__ == "__main__":
    # # Load and clean data
    # pardir = os.path.dirname(os.getcwd())
    # df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    # #df = pd.read_csv("Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    # df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
    #               'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    # df = ut.clean_data(df)
    # df = ut.add_hours_bef_arr(df)
    # df = ut.erp_before_ata(df) # remove if you use for all
    # df = ut.ais_before_erp(df) # remove if you use for all
    
    # df.to_csv("tbl_ship_arrivals_log_202103_cleaned.csv", index = False)
    
    df = pd.read_csv("data\\tbl_ship_arrivals_log_202103_cleaned.csv", low_memory=False)
    print('df')
    df = ut.add_eta_error(df)
    
    bracketwidth = 5
    percent = 1
    
    #my_filters = {'erp_bef_ata': False}
    my_filters = {}
    mean_erp, mean_ais = plot_relative_error("relative_error_no_filter", df, 
                                              my_filters, bracketwidth = bracketwidth, 
                                              percent = percent)
    
    
    
# =============================================================================
#     90 percent
# =============================================================================
    
    # filters = my_filters
    # bracketwidth = 5 
    # percent = 0.9
    
    # # Use filters
    # df_filter = df
    # for key in filters.keys():
    #     df_filter = df_filter[df_filter[key] == filters[key]]
    
    
    # track_ids = df_filter.track_id.unique()
    # n = len(track_ids)
    
    # # Determining the maximum amount of hours away we have data for
    # max_hours = np.zeros(n)
    # for i in range(n):
    #     max_hours[i] = ut.max_hour(df_filter, track_ids[i])
    
    # # Maximum amount of points
    # points = int(np.ceil(np.max(max_hours)/bracketwidth) + 1) 
    # mean_erp = np.zeros(points)
    # mean_ais = np.zeros(points)
    
    # ais_diff_list = np.zeros(0)
    # erp_diff_list = np.zeros(0)
    
    # for i in range(n):
    #     ata = ut.ata_Extract(df, track_ids[i]).astype('datetime64[s]')
        
    #     df_small = df_filter[df_filter["track_id"]==track_ids[i]]
    #     ais = df_small["eta_ais"].to_numpy().astype(str)
    #     idx = ais != 'nan'
    #     ais_diff = np.ones(len(ais))*np.nan
    #     ais_diff[idx] = np.abs(ata - ais[idx].astype('datetime64[s]'))
    #     ais_diff_list = np.concatenate((ais_diff_list, ais_diff))
        
    #     erp = df_small["eta_erp"].to_numpy().astype(str)
    #     idx = erp != 'nan'
    #     erp_diff = np.ones(len(ais))*np.nan
    #     erp_diff[idx] = np.abs(ata - erp[idx].astype('datetime64[s]'))
    #     erp_diff_list = np.concatenate((erp_diff_list, erp_diff))
        
        
    # df_filter['erp_error'] = erp_diff_list
    # df_filter['ais_error'] = ais_diff_list
    
    # ### ais hourly percentage ###
    # time_low = 0
    # time_high = bracketwidth
    # for i in range(points):
    #     erp_error, ais_error = Extract_time_brackets_all_tracks(df_filter, time_low, time_high)
    #     divisor = 1/((time_low + time_high)*3600/2)
        
    #     erp_error = erp_error.astype(float)
    #     ais_error = ais_error.astype(float)
        
    #     mean_erp[i] = np.mean(erp_error*divisor)
        
    #     ais_length = int(len(ais_error)*percent)
    #     print(ais_length)
    #     ais_error = np.sort(ais_error)[:ais_length]
    #     mean_ais[i] = np.mean(ais_error*divisor)
        
    #     time_low += bracketwidth
    #     time_high += bracketwidth
    
# =============================================================================
#     Uden percent
# =============================================================================
    # df_filter = df[df['erp_bef_ata'] == False]
    
    # # Determines the track id's and amount of track id's
    # track_ids = df_filter.track_id.unique()
    # n = len(track_ids)
    
    # # Determining the maximum amount of hours away we have data for
    # max_hours = np.zeros(n)
    # for i in range(n):
    #     max_hours[i] = ut.max_hour(df_filter, track_ids[i])
    
    
    # # Bracketwidth can be changed
    # bracketwidth = 5
    
    # # Maximum amount of points
    # points = int(np.ceil(np.max(max_hours)/bracketwidth) + 1) 
    # erp_est = np.zeros((n, points))
    # ais_est = np.zeros((n, points))
    
    # # Creates matrix of time differences
    # for i in range(1):
    #     length = int(np.ceil(max_hours[i]/bracketwidth) + 1)
    #     time_low = 0 # in hours
    #     time_high = bracketwidth # in hours
    #     ata_ais = ut.ata_Extract(df, track_ids[i])
    #     for j in range(length):
    #         erp, ais = ut.Extract_time_brackets(df_filter, time_low, time_high, track_ids[i]) 
    
    #         k = len(erp)
    #         l = len(ais)
    #         divisor = (time_low + time_high)*3600/2 # in seconds
    #         print(divisor)
    #         if k != 0:
    #             erp_est[i, j] = np.sum(ut.time_difference_array(erp, ata_ais).astype(int))/k
    #             erp_est[i, j] = erp_est[i, j]/divisor
                
    #         if l != 0:
    #             ais_est[i, j] = np.sum(ut.time_difference_array(ais, ata_ais).astype(int))/l
    #             ais_est[i, j] = ais_est[i, j]/divisor
    
    #         time_low += bracketwidth
    #         time_high += bracketwidth
    #     print(i)
    
    
    # # Sum points in the same times and means
    # mean_ais = np.zeros(points)
    # mean_erp = np.zeros(points)
    # for i in range(points):
    #     mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) 
    #     mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 
    
    # zoom = points
    # x_ticks = []
    # for i in range(points):
    #       a = i*bracketwidth
    #       tic = "{}-{}".format(a, a + bracketwidth)
    #       x_ticks.append(tic)
    
    # #time = np.linspace(0, np.max(max_hours), points)
    # fig, ax = plt.subplots()
    # plt.style.use('seaborn-darkgrid')
    # ax.plot(x_ticks, mean_erp, label='eta_erp')
    # ax.plot(x_ticks, mean_ais, label='eta_ais')
    # ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
    # ax.invert_xaxis()
    # ax.set_ylabel("Absolute error in hours")
    # ax.set_xlabel('Hours before arrival')
    # plt.legend(["eta_erp","eta_ais"])
    # plt.savefig("figures/relative/relative_error_no_filter_90")
    # plt.show()