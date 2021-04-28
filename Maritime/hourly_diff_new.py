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
    
    eta_erp = eta_erp.unique().astype(str)
    eta_ais = eta_ais.unique().astype(str)
    
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

points = int(np.ceil(np.max(max_hours)/bracketwidth))
erp_est = np.zeros((n, points))
ais_est = np.zeros((n, points))

for i in range(n):
   length = int(np.ceil(max_hours[i]/bracketwidth))
   time_low = 0
   time_high = 5
   ata_ais = ut.ata_Extract(df, track_ids[i])
   for j in range(length):
       erp, ais = Extract_time_brackets(df, time_low, time_high, track_ids[i])
       time_low += 5
       time_high += 5
       k = len(erp)
       l = len(ais)
       if k != 0:
           for n in range(k):
               erp_est[i, j] += ut.TimeDifference(erp[n], ata_ais[0])/k
       # else:
       #     erp_est[i, j] = erp_est[i-1, j]
       if l != 0:
           for n in range(l):
               ais_est[i, j] += ut.TimeDifference(ais[n], ata_ais[0])/l
       # else:
       #     ais_est[i, j] = ais_est[i-1, j]


mean_ais = np.zeros(points)
mean_erp = np.zeros(points)
for i in range(points):
    mean_erp[i] = np.sum(erp_est[:,i])/(np.count_nonzero(erp_est[:,i]))
    mean_ais[i] = np.sum(ais_est[:,i])/(np.count_nonzero(ais_est[:,i]))

#%%
plt.plot(mean_ais/(120))
plt.plot(mean_erp/(120))
plt.show()
