import pandas as pd
import numpy as np
from datetime import datetime

#%%
df = pd.read_csv("Maritime/data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

# remove ships that has not arrived
df_arrive = df[df['status'] == 14]
df = df[df['track_id'].isin(df_arrive['track_id'])]

# remove ships that only has status 14 in the log
df_eta = df[df['status'] != 14]
df = df[df['track_id'].isin(df_eta['track_id'])]
df = df.sort_values(by=['track_id', 'stamp'])

# Har tilføjet day og hour for jeg tænkte vi kunne bruge det til at kategorisere dataen.
# ift. han gerne ville have når de er 10 timer væk klare de det så godt osv.
# Det kan nok også bruges til at extracte effektivt selvom jeg ikke helt har gennemskuet hvordan

df['hour'] = pd.to_datetime(df['stamp']).dt.hour
df['day'] = pd.to_datetime(df['stamp']).dt.day
#df1.duration = df1.duration / 60

# functionen skal lige nu have to timestaps i vores format.
# Så hvis vi har en god måde at hente dem er det cool.
def TimeDifference(time_1,time_2):
    """
    Calculates absolute time difference between two timestamps in the 
    YYYY-mm-dd HH:MM:SS format.
    """
    FMT = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(time_1, FMT) - datetime.strptime(time_2, FMT)
    sek_diff = tdelta.days * 24 * 3600 + tdelta.seconds
    return abs(sek_diff)

time_1 = "2021-03-16 17:02:28"
time_2 = "2021-03-18 10:14:55"
sek_diff = TimeDifference(time_1, time_2)

Unique_track_ids = df.track_id.unique()

def TimeExtract(df, hour, day):
    """
    Extracts the eta_erp, eta_ais and ata_ais on a given time for a dataframe

    """
    
    return 1
