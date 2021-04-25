import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import time_func as tf


#%%
# Load data
pardir = os.path.dirname(os.getcwd())
df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']
    
df = tf.clean_data(df)
    
# Tilføjet day og hour for jeg tænkte vi kunne bruge det til at kategorisere dataen.
df['hour'] = pd.to_datetime(df['stamp']).dt.hour
df['day'] = pd.to_datetime(df['stamp']).dt.day
track_ids = df.track_id.unique()
    


#%% Trip lengths
n = len(track_ids)
j = 0
trip_lengths = np.zeros(n)
for track_id in track_ids:
    tmp = 0
    days = tf.Day_trackid(df, track_id)
    for day in days:
        hours = tf.Hour_trackid(df, track_id, day)
        tmp += len(hours)
    trip_lengths[j] = tmp
    j+=1

#%% Finding the differences
longest_trip = int(np.max(trip_lengths))
difference_ais = np.zeros((n, longest_trip))
difference_erp = np.zeros((n, longest_trip))

j = 0
for track_id in track_ids:
    i = 0
    ata = tf.ata_Extract(df, track_id)
    days = tf.Day_trackid(df, track_id)
    for day in days:
        hours = tf.Hour_trackid(df, track_id, day)
        for hour in hours:
            eta_erp, eta_ais = tf.eta_Extract(df, hour, day, track_id)
            k = len(eta_erp)
            l = len(eta_ais)
            if k != 0:
                for eta in eta_erp:
                    difference_erp[j, i] += tf.TimeDifference(eta, ata[0])/k
            if l !=0:
                for eta in eta_ais:
                    difference_ais[j, i] += tf.TimeDifference(eta, ata[0])/l        
            i+=1
    j+=1        
            
#%% Meaning
mean_ais = np.zeros(longest_trip)
mean_erp = np.zeros(longest_trip)
for i in range(longest_trip):
    mean_erp[i] = np.sum(difference_erp[:,i])/(np.count_nonzero(difference_erp[:,i]))
    mean_ais[i] = np.sum(difference_ais[:,i])/(np.count_nonzero(difference_ais[:,i]))
    
#%% Plotting
time = [i for i in range(432)]
tickets = [i*40 for i in range(int(np.floor(432/40)))]
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots(1, 2, sharex=True, sharey=True, figsize=(8,4))
ax[0].bar(time, mean_ais)
ax[1].bar(time, mean_erp)
ax[0].set_title("Eta_ais")
ax[1].set_title("Eta_erp")
ax[0].set_xlabel("Hour")
ax[1].set_xlabel("Hour")
ax[0].set_ylabel("Absolute time difference")
ax[0].set_xticks(tickets)
ax[1].set_xticks(tickets)
fig.subplots_adjust(hspace=0.1, wspace=0.1)
plt.savefig(pardir + "/Maritime/figures/hourlydiff.pdf")
plt.show()