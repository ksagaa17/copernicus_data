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
def time_difference_array(time1, time2):
    

def relative_error(df, filters, bracketwidth = 5):
    
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
    erp_est = np.zeros((n, points))
    ais_est = np.zeros((n, points))
    
    for i in range(n):
        length = int(np.ceil(max_hours[i]/bracketwidth) + 1)
        time_low = 0 # in hours
        time_high = bracketwidth # in hours
        ata_ais = ut.ata_Extract(df, track_ids[i])[0]
        for j in range(length):
            erp, ais = ut.Extract_time_brackets(df_filter, time_low, time_high, track_ids[i]) 
    
            k = len(erp)
            l = len(ais)
            divisor = (time_low + time_high)*3600/2 # in seconds
            if k != 0: 
                for n in range(k):
                    erp_est[i, j] += ut.TimeDifference(erp[n], ata_ais)/k
                erp_est[i, j] = erp_est[i, j]/divisor
            if l != 0:
                for n in range(l):
                    ais_est[i, j] += ut.TimeDifference(ais[n], ata_ais)/l
                ais_est[i, j] = ais_est[i, j]/divisor
    
            time_low += bracketwidth
            time_high += bracketwidth
    
    
    # Sum points in the same times and means
    mean_ais = np.zeros(points)
    mean_erp = np.zeros(points)
    for i in range(points):
        mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) 
        mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 
    
    return mean_erp, mean_ais


def plot_relative_error(figname, df, filters, bracketwidth = 5, zoom = None, returns = True):
    mean_erp, mean_ais = relative_error(df, filters, bracketwidth = bracketwidth)
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
    plt.savefig("figures/"+ figname + "{0}".format(zoom))
    plt.show()
    
    if returns == True:
        return mean_erp, mean_ais

if __name__ == "__main__":
    # Load and clean data
    pardir = os.path.dirname(os.getcwd())
    df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    #df = pd.read_csv("Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                  'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    df = ut.clean_data(df)
    df = ut.add_hours_bef_arr(df)
    df = ut.erp_before_ata(df) # remove if you use for all
    df = ut.ais_before_erp(df) # remove if you use for all

    # my_filters = {}
    # mean_erp, mean_ais = plot_relative_error("relative_error_no_filters", df, my_filters)

    df_filter = df[df['erp_bef_ata'] == False]
    
    # Determines the track id's and amount of track id's
    track_ids = df_filter.track_id.unique()
    n = len(track_ids)
    
    # Determining the maximum amount of hours away we have data for
    max_hours = np.zeros(n)
    for i in range(n):
        max_hours[i] = ut.max_hour(df_filter, track_ids[i])
    
    
    # Bracketwidth can be changed
    bracketwidth = 5
    
    # Maximum amount of points
    points = int(np.ceil(np.max(max_hours)/bracketwidth) + 1) 
    erp_est = np.zeros((n, points))
    ais_est = np.zeros((n, points))
    
    # Creates matrix of time differences
    for i in range(n):
        length = int(np.ceil(max_hours[i]/bracketwidth) + 1)
        time_low = 0 # in hours
        time_high = bracketwidth # in hours
        ata_ais = ut.ata_Extract(df, track_ids[i])[0]
        for j in range(length):
            erp, ais = ut.Extract_time_brackets(df_filter, time_low, time_high, track_ids[i]) 
    
            k = len(erp)
            l = len(ais)
            divisor = (time_low + time_high)*3600/2 # in seconds
            if k != 0: 
                for n in range(k):
                    erp_est[i, j] += ut.TimeDifference(erp[n], ata_ais)/k
                erp_est[i, j] = erp_est[i, j]/divisor
            if l != 0:
                for n in range(l):
                    ais_est[i, j] += ut.TimeDifference(ais[n], ata_ais)/l
                ais_est[i, j] = ais_est[i, j]/divisor
    
            time_low += bracketwidth
            time_high += bracketwidth
    
    
    # Sum points in the same times and means
    mean_ais = np.zeros(points)
    mean_erp = np.zeros(points)
    for i in range(points):
        mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) 
        mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 
    
    zoom = points
    x_ticks = []
    for i in range(points):
          a = i*bracketwidth
          tic = "{}-{}".format(a, a + bracketwidth)
          x_ticks.append(tic)
    
    #time = np.linspace(0, np.max(max_hours), points)
    fig, ax = plt.subplots()
    plt.style.use('seaborn-darkgrid')
    ax.plot(x_ticks, mean_erp, label='eta_erp')
    ax.plot(x_ticks, mean_ais, label='eta_ais')
    ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
    ax.invert_xaxis()
    ax.set_ylabel("Absolute error in hours")
    ax.set_xlabel('Hours before arrival')
    plt.legend(["eta_erp","eta_ais"])
    #plt.savefig("figures/hourlydiff_new_{0}".format(zoom))
    plt.show()