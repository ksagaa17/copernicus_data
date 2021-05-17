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


#%% Absolute Difference
month = [1,2,3]
suez = False
df = ut.get_data_all_month_cleaned()
if suez == True:
    stamps = df['stamp'].to_numpy().astype(np.datetime64)
    df = df.loc[stamps >= np.datetime64('2021-03-23T00:00')]

percent = 0.9
bracketwidth = 5 
filters = {}#{'erp_bef_ata': True, 'ais_bef_erp': False} #{'erp_is_nan': True} 
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

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.plot(x_ticks[:zoom], (mean_erp/(60*60))[:zoom], label='eta_erp')
ax.plot(x_ticks[:zoom], (mean_ais/(60*60))[:zoom], label='eta_ais')
ax.xaxis.set_major_locator(mticker.MaxNLocator(6))
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta_erp","eta_ais"])
plt.savefig("figures/hourlydiff_bw{0}_pct{1}_zoom{2}_month{3}_filter{4}".format(bracketwidth, int(percent*100), zoom, month, filters))
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
