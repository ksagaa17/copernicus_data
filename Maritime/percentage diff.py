import utillities as ut
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

#%%
# Load and clean data
pardir = os.path.dirname(os.getcwd())
df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
#df = pd.read_csv("Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
df = ut.clean_data(df)
df = ut.add_hours_bef_arr(df)

# Determines the track id's and amount of track id's
track_ids = df.track_id.unique()
n = len(track_ids)

# Determining the maximum amount of hours away we have data for
max_hours = np.zeros(n)
for i in range(n):
    max_hours[i] = ut.max_hour(df, track_ids[i])
    
# Bracketwidth can be changed
bracketwidth = 5

# Maximum amount of points
points = int(np.ceil(np.max(max_hours)/bracketwidth)+1) 
erp_est = np.zeros((n, points))
ais_est = np.zeros((n, points))

# Creates matrix of time differences
for i in range(n):
   length = int(np.ceil(max_hours[i]/bracketwidth)+1)
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

# Sum points in the same times and means
mean_ais = np.zeros(points)
mean_erp = np.zeros(points)
for i in range(points):
    mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) 
    mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 

#%% Plotting
zoom = points
x_ticks = []
for i in range(points):
     a = i*bracketwidth
     tic = "{}-{}".format(a, a + bracketwidth)
     x_ticks.append(tic)

#time = np.linspace(0, np.max(max_hours), points)
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


