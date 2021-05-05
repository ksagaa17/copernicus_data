import utillities as ut
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#%%
def absolute_error(track_ids, df, bracketwidth = 5, cleaned = True):
    """
    Extracts the eta_erp and eta_ais for a given track_id for a dataframe. 
    Returns these in numpy arrays.

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
    points = int(np.ceil(np.max(max_hours)/bracketwidth)) 
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

#%% 
pardir = os.path.dirname(os.getcwd())
df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
# df = pd.read_csv("Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
df = ut.clean_data(df)
df = ut.add_hours_bef_arr(df)
df = ut.erp_before_ata(df) # Only nessescary when cleaned = True
df = ut.ais_before_erp(df) # Only nessescary when cleaned = True
track_ids = df.track_id.unique()
bracketwidth = 5 
mean_erp, mean_ais = absolute_error(track_ids, df, bracketwidth, cleaned = True)

#%% plotting
total_points = len(mean_erp)
zoom = total_points
x_ticks = []
for i in range(total_points):
     a = i*bracketwidth
     tic = "{}-{}".format(a, a + bracketwidth)
     x_ticks.append(tic)

fig, ax = plt.subplots()
plt.style.use('seaborn-darkgrid')
ax.plot(x_ticks[:zoom], (mean_erp/(60*60))[:zoom], label='eta_erp')
ax.plot(x_ticks[:zoom], (mean_ais/(60*60))[:zoom], label='eta_ais')
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta_erp","eta_ais"])
plt.savefig("figures/hourlydiff_new_{0}".format(zoom))
plt.show()

#%% Percentage
# percent_ais = np.zeros(points)
# percent_erp = np.zeros(points)

# 85 may change dependent on whether or not the data is cleaned and the bracketwidth
# for i in range(points-1):
#     percent_ais[i+1] = 100*(mean_ais[85]- mean_ais[i+1])/mean_ais[85] 
#     percent_erp[i+1] = 100*(mean_erp[85]- mean_erp[i+1])/mean_erp[85]

# zoom = points
# fig, ax = plt.subplots()
# plt.style.use('seaborn-darkgrid')
# ax.plot(x_ticks[1:zoom], percent_erp[1:zoom], label = 'eta_erp')
# ax.plot(x_ticks[1:zoom], percent_ais[1:zoom], label = 'eta_ais')
# ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
# ax.invert_xaxis()
# ax.set_ylabel("Percentage improvement [%]")
# ax.set_xlabel('Hours before arrival')
# plt.legend(["eta_erp","eta_ais"])
# plt.savefig("figures/percent_improvement_new_{0}".format(zoom))
# plt.show()
