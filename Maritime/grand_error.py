# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:53:04 2021

@author: krist
"""

import numpy as np
import pandas as pd
import utillities as util
import matplotlib.pyplot as plt

def grand_error(df, percent=1, plot_hist=False):
    """
    Computes the mean and standard diviation of the absolute error of the etas.

    Parameters
    ----------
    df : panda dataframe
        cleaned Log fra ETA1.
    percent : float, optional
        Number specifiyng the percent of data we want to use in the calculations
        must be between 0 and 1
    plot_hist : boolean, optional
        Whether to show histograms of absolute error. The default is False.

    Returns
    -------
    mae_ais : float
        Mean absolute error of eta_ais.
    std_ais : float
        Standard deviation of absolute error of eta_ais.
    mae_erp : float
        Mean absolute error of eta_erp.
    std_erp : float
        Standard deviation of absolute error of eta_erp.

    """
    
    track_ids = df.track_id.unique()   
    
    abs_error_erp = np.array([])
    abs_error_ais = np.array([])
    for track_id in track_ids:
        ata_ais = util.ata_Extract(df, track_id)[0]
        eta_erp, eta_ais = util.eta_Extract_whole_track(df, track_id)
        
        time_diff = []
        for eta in eta_erp:
            time_diff.append(util.TimeDifference(eta,ata_ais))
        
        abs_error_erp = np.concatenate((abs_error_erp, np.array(time_diff)))
        
        time_diff = []
        for eta in eta_ais:
            time_diff.append(util.TimeDifference(eta,ata_ais))
        
        abs_error_ais = np.concatenate((abs_error_ais, np.array(time_diff)))
        
    abs_error_erp = abs_error_erp/3600       # in hours
    abs_error_ais = abs_error_ais/3600       # in hours
    
    print(len(abs_error_ais))
    abs_error_ais = np.sort(abs_error_ais)[:int(percent*len(abs_error_ais))]
    print(len(abs_error_ais))
          
    mae_erp = np.mean(abs_error_erp)
    mae_ais = np.mean(abs_error_ais)
    
    std_erp = np.sqrt(np.var(abs_error_erp))
    std_ais = np.sqrt(np.var(abs_error_ais))
    
    if plot_hist == True:
        plt.figure()
        plt.hist(abs_error_ais)
        plt.show()
        
        plt.figure()
        plt.hist(abs_error_erp)
        plt.show()
    
    return mae_ais, std_ais, mae_erp, std_erp


if __name__ == "__main__":
    # =========================================================================
    #     Compute grand mean and standard deviation using all relavant data
    # =========================================================================
    df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                  'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

    df = util.clean_data(df)

    mae_ais, std_ais, mae_erp, std_erp = grand_error(df, percent=0.5, plot_hist=False)
    
    
    # #%%
    # # =========================================================================
    # #     Compute grand mean for data before Suez Crisis (before 2021-03-23)
    # # =========================================================================
    # df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    # df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
    #               'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    
    # stamps = df['ata_ais'].to_numpy().astype(np.datetime64)
    # df = df.loc[stamps <= np.datetime64('2021-03-23T00:00')]
    
    # df = clean.clean_data(df)

    # mae_ais, std_ais, mae_erp, std_erp = grand_error(df, plot_hist=False)
    
    # #%%
    # # =========================================================================
    # #     Compute grand mean for data after Suez Crisis (after 2021-03-23)
    # # =========================================================================
    # df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    # df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
    #               'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    
    # stamps = df['stamp'].to_numpy().astype(np.datetime64)
    # df = df.loc[stamps >= np.datetime64('2021-03-23T00:00')]
    
    # df = clean.clean_data(df)

    # mae_ais, std_ais, mae_erp, std_erp = grand_error(df, plot_hist=False)
    
    
    

