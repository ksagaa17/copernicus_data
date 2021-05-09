import utillities as ut
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


def absolute_error(df, filters = {'erp_bef_ata': True, 'ais_bef_erp': False}, percent = 0, bracketwidth = 5):
    """
    calculate the mean aboslute error for the erp_eta and the ais_eta.

    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    filter : dictionary
        whether or no the data should be cleaned
    bracketwidth : int
        width of the error brackets
    
    Returns
    -------
    mean_erp : ndarray
    Contains the mean absolute time difference for the eta_erp
    
    mean_ais : ndarray
    Contains the mean absolute time difference for the eta_ais
    """
    
    #print("Warning this function has yet to be optimised so grab a cup of coffe or a snack")
    
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
    points = int(np.ceil(np.max(max_hours)/bracketwidth)+1) 
    mean_erp = np.zeros(points)
    mean_ais = np.zeros(points)
    
    ### ais hourly percentage ###
    time_low = 0
    time_high = bracketwidth
    for i in range(points):
        erp_error, ais_error = ut.Extract_time_brackets_all_tracks(df_filter, time_low, time_high)
        
        erp_error = erp_error.astype(float)
        ais_error = ais_error.astype(float)
        
        mean_erp[i] = np.mean(erp_error)
        
        ais_length = int(len(ais_error)*percent)        
        ais_error = np.sort(ais_error)[:ais_length]
        mean_ais[i] = np.mean(ais_error)
        
        time_low += bracketwidth
        time_high += bracketwidth
    
    return mean_erp, mean_ais


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


#%% Absolute Difference
month = 3
df = ut.get_data_cleaned(month)
percent = 1
bracketwidth = 5 
filters = {'erp_bef_ata': True, 'ais_bef_erp': False} #{'erp_is_nan': True} 
mean_erp, mean_ais = absolute_error(df, filters = filters,
                                    percent = percent, bracketwidth = bracketwidth)

#%% Plotting
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
plt.savefig("figures/hourlydiff_{0}_{1}_{2}_{3}".format(bracketwidth, int(percent*100), zoom, month))
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
