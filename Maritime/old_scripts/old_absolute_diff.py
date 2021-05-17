import numpy as np
import utilities as ut

def absolute_error_old(track_ids, df, bracketwidth = 5, cleaned = True):
    """
    calculate the mean aboslute error for the erp_eta and the ais_eta.

    Parameters
    ----------
    track_ids : ndarray
        unique track ids
    bracketwidth : int
        width of the error brackets
    df : pandas dataframe
        Log fra ETA1.
    cleaned : Logical value
        whether or no the data should be cleaned
    
    Returns
    -------
    mean_erp : ndarray
    Contains the mean absolute time difference for the eta_erp
    
    mean_ais : ndarray
    Contains the mean absolute time difference for the eta_ais
    """
    
    print("Warning this function has yet to be optimised so grab a cup of coffe or a snack")
    n = len(track_ids)
    # Determining the maximum amount of hours away we have data for
    max_hours = np.zeros(n)
    for i in range(n):
        max_hours[i] = ut.max_hour(df, track_ids[i])
    
    # Maximum amount of points
    points = int(np.ceil(np.max(max_hours)/bracketwidth)+1) 
    erp_est = np.zeros((n, points))
    ais_est = np.zeros((n, points))
    
    if cleaned == True: 
        # Creates matrix of time differences
        for i in range(n):
            length = int(np.ceil(max_hours[i]/bracketwidth))
            time_low = 0 
            time_high = bracketwidth
            ata_ais = ut.ata_Extract(df, track_ids[i])[0]
            
            for j in range(length):
                erp = ut.Extract_time_brackets_erp(df, time_low, time_high, track_ids[i]) 
                ais = ut.Extract_ais_specific(df, time_low, time_high, track_ids[i])
                time_low += bracketwidth
                time_high += bracketwidth
                k = len(erp)
                l = len(ais)
                
                if k != 0: 
                    for n in range(k):
                        erp_est[i, j] += ut.TimeDifference(erp[n], ata_ais)/k 
                
                if l != 0:
                    for n in range(l):
                        ais_est[i, j] += ut.TimeDifference(ais[n], ata_ais)/l 
        
        mean_ais = np.zeros(points)
        mean_erp = np.zeros(points)
        for i in range(points):
            mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) 
            mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 
    
    else:
        # Creates matrix of time differences
        for i in range(n):
            length = int(np.ceil(max_hours[i]/bracketwidth))
            time_low = 0 
            time_high = bracketwidth
            ata_ais = ut.ata_Extract(df, track_ids[i])[0]
            
            for j in range(length):
                erp, ais = ut.Extract_time_brackets(df, time_low, time_high, track_ids[i])
                time_low += bracketwidth
                time_high += bracketwidth
                k = len(erp)
                l = len(ais)
            
                if k != 0: 
                    for n in range(k):
                        erp_est[i, j] += ut.TimeDifference(erp[n], ata_ais)/k 
                
                if l != 0:
                    for n in range(l):
                        ais_est[i, j] += ut.TimeDifference(ais[n], ata_ais)/l 

        mean_ais = np.zeros(points)
        mean_erp = np.zeros(points)
        for i in range(points):
            mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) 
            mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 
    
    return mean_erp, mean_ais