import pandas as pd
import numpy as np
from datetime import datetime
import os

#%%
def TimeDifference(time_1,time_2):
    """
    Calculates absolute time difference between two timestamps in the 
    YYYY-mm-dd HH:MM:SS format.
    """
    FMT = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(time_1, FMT) - datetime.strptime(time_2, FMT)
    sek_diff = tdelta.days * 24 * 3600 + tdelta.seconds
    return abs(sek_diff)


def Day_trackid(df, track_id):
    """
    extracts days for a given track_id of a dataframe
    """
    indexes = df.query('track_id == {0}'.format(track_id)).index
    #hours = df['hour'][indexes]
    days = df['day'][indexes]
    
    #hours = hours.unique()  
    days = days.unique()  
    return days


def Hour_trackid(df, track_id, day):
    """
    extracts hours for a given track_id and day of a dataframe
    """
    indexes = df.query('track_id == {0} & day == {1}'.format(track_id, day)).index
    hours = df['hour'][indexes] 
    hours = hours.unique()    
    return hours


def ata_Extract(df, track_id):
     """
     Extracts the ata_ais for a given track_id for a dataframe

     """
     indexes = df.query('track_id == {0}'.format(track_id)).index
     ata_ais = df['ata_ais'][indexes]
     ata_ais = ata_ais.unique()
     return ata_ais


def eta_Extract(df, hour, day, track_id):
    """
    Extracts the eta_erp and eta_ais at a given time and track_id for a dataframe

    """
    indexes = df.query('hour == {0} & day == {1} & track_id == {2}'.format(hour, day, track_id)).index
    eta_erp = df['eta_erp'][indexes]
    eta_ais = df['eta_ais'][indexes]
    
    eta_erp = eta_erp.unique()  
    eta_ais = eta_ais.unique()
    return eta_erp, eta_ais


#%%
# Load data
pardir = os.path.dirname(os.getcwd())
df = pd.read_csv(pardir + "\\Maritime\\data\\tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

#Cleaning
# remove ships that has not arrived alla Kristian
df_arrive = df[df['status'] == 14]
df = df[df['track_id'].isin(df_arrive['track_id'])]

# remove ships that only has status 14 in the log alla Kristian
df_eta = df[df['status'] != 14]
df = df[df['track_id'].isin(df_eta['track_id'])]
df = df.sort_values(by=['track_id', 'stamp'])

# Tilføjet day og hour for jeg tænkte vi kunne bruge det til at kategorisere dataen.
df['hour'] = pd.to_datetime(df['stamp']).dt.hour
df['day'] = pd.to_datetime(df['stamp']).dt.day

#Test time Difference
time_1 = "2021-03-16 17:02:28"
time_2 = "2021-03-18 10:14:55"
sek_diff = TimeDifference(time_1, time_2)

#Test day_trackid og hour_track_id
track_ids = df.track_id.unique()
days = Day_trackid(df, 4359391821106)
hours = Hour_trackid(df, 4359391821106, 1)

# Test time extract
eta_erp, eta_ais = eta_Extract(df, 8, 1, 4359391821106)
ata_ais = ata_Extract(df, 4359391821106)
