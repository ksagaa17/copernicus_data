# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 13:53:04 2021

@author: krist
"""

import numpy as np
import pandas as pd
import time_func1 as tf
import extract_function as clean
import matplotlib.pyplot as plt

def grand_error(df, plot_hist=False):
    """
    Computes the mean and standard diviation of the absolute error of the etas.

    Parameters
    ----------
    df : panda dataframe
        Uncleaned Log fra ETA1..
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
    df = clean.clean_data(df)
    track_ids = df.track_id.unique()   
    
    abs_error_erp = np.array([])
    abs_error_ais = np.array([])
    for track_id in track_ids:
        ata_ais = tf.ata_Extract(df, track_id)[0]
        eta_erp, eta_ais = tf.eta_Extract_whole_track(df, track_id)
        
        time_diff = []
        for eta in eta_erp:
            time_diff.append(tf.TimeDifference(eta,ata_ais))
        
        abs_error_erp = np.concatenate((abs_error_erp, np.array(time_diff)))
        
        time_diff = []
        for eta in eta_ais:
            time_diff.append(tf.TimeDifference(eta,ata_ais))
        
        abs_error_ais = np.concatenate((abs_error_ais, np.array(time_diff)))
        
    abs_error_erp = abs_error_erp/3600       # in hours
    abs_error_ais = abs_error_ais/3600       # in hours

    mae_erp = np.mean(abs_error_erp)
    mae_ais = np.mean(abs_error_ais)
    
    std_erp = np.sqrt(np.var(abs_error_erp))
    std_ais = np.sqrt(np.var(abs_error_ais))
    
    if plot_hist == True:
        plt.figure()
        plt.hist(abs_error_ais)
        plt.show()
    
    return mae_ais, std_ais, mae_erp, std_erp
    

if __name__ == "__main__":
    df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
    df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
                  'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    
    df = clean.clean_data(df)
    
    track_ids = df.track_id.unique()
    
    # liste = []
    # for tr in track_ids:
    #     liste.append(len(tf.ata_Extract(df, tr)))
    
    mae_ais, std_ais, mae_erp, std_erp = grand_error(df, plot_hist=True)

