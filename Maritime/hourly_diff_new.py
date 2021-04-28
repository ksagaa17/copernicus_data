import utillities as ut
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def Extract_time_brackets(df, time_low, time_high, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time frame and track_id
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    time_low : int
        time before arrival lower bound
    time_high : int
        time before arrival upper bound
    track_id : int
        A track_id from df.

    Returns
    -------
    eta_erp : ndarray
        eta_erp for the given track_id.
    eta_ais : ndarray
        eta_ais for the given track_id.
    """
    
    indexes = df.query('hours_bef_arr >= {0} & hours_bef_arr < {1} & track_id == {2}'.format(time_low, time_high, track_id)).index
    eta_erp = df['eta_erp'][indexes]
    eta_ais = df['eta_ais'][indexes]
    
    eta_erp = eta_erp.astype(str).to_numpy()
    eta_ais = eta_ais.astype(str).to_numpy()
    
    eta_erp = eta_erp[eta_erp != 'nan']
    eta_ais = eta_ais[eta_ais != 'nan']
    return eta_erp, eta_ais


def max_hour(df, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time frame and track_id
    Parameters
    ----------
    df : pandas dataframe
        Log fra ETA1.
    track_id : int
        A track_id from df.

    Returns
    -------
    max_hour : int
        maximum hour before arrvival.
    """
    
    indexes = df.query('track_id == {0}'.format(track_id)).index
    hours_before = df['hours_bef_arr'][indexes]
    max_hours = hours_before.max()
    return max_hours

#%%
# Load data
pardir = os.path.dirname(os.getcwd())
df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
#df = pd.read_csv("Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

df = ut.clean_data(df)
df = ut.add_hours_bef_arr(df)
track_ids = df.track_id.unique()
n = len(track_ids)
max_hours = np.zeros(n)
for i in range(n):
    max_hours[i] = max_hour(df, track_ids[i])
    
bracketwidth = 5

points = int(np.ceil(np.max(max_hours)/bracketwidth)+1) #maximum antal punkter
erp_est = np.zeros((n, points)) # laver en række for hver track_id
ais_est = np.zeros((n, points))

for i in range(n):
   length = int(np.ceil(max_hours[i]/bracketwidth)+1) # antal punkter for et track_id
   time_low = 0 
   time_high = bracketwidth # time brackets
   ata_ais = ut.ata_Extract(df, track_ids[i])[0]
   for j in range(length):
       erp, ais = Extract_time_brackets(df, time_low, time_high, track_ids[i])
       time_low += bracketwidth
       time_high += bracketwidth # nye brackéts
       k = len(erp) # da den skal bruges flere gange
       l = len(ais)
       if k != 0: # i tilfælde af der ikke er data
           for n in range(k):
               erp_est[i, j] += ut.TimeDifference(erp[n], ata_ais)/k # ligger time diff til i indgang for track_id og time bracket
       if l != 0:
           for n in range(l):
               ais_est[i, j] += ut.TimeDifference(ais[n], ata_ais)/l # same men for ais_est

mean_ais = np.zeros(points)
mean_erp = np.zeros(points)
for i in range(points):
    mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i])) # summere for alle track_ids i samme brackets og dividere med antal ikke nul indgange
    mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i])) 

#%%
time = np.linspace(0, np.max(max_hours), points)

fig, ax = plt.subplots()
ax.plot(time, mean_erp/(120*24), label='eta_erp')
ax.plot(time, mean_ais/(120*24), label='eta_ais')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in days")
ax.set_xlabel('Hours before arrival')
plt.show()
