import pandas as pd
import numpy as np
from datetime import datetime

#%%

df1 = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df1.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

df1 = df1.sort_values(by=['track_id'])
track_id = df1['track_id'].to_numpy()
number_of_ids = len(np.unique(track_id))

status = df1['status'].to_numpy()
arrivals = np.sum(status == 14)

df_arrive = df1.loc[df1['status'] == 14]

df_small = df1.loc[df1['track_id'].isin(df_arrive['track_id'])]

df_eta = df_small.loc[df_small['status'] != 14]

df_final = df_small.loc[df_small['track_id'].isin(df_eta['track_id'])]

#%%
# Har tilføjet day og hour for jeg tænkte vi kunne bruge det til at kategorisere dataen.
# ift. han gerne ville have når de er 10 timer væk klare de det så godt osv.
# Det kan nok også bruges til at extracte effektivt selvom jeg ikke helt har gennemskuet hvordan

df1['hour'] = pd.to_datetime(df1['stamp']).dt.hour
df1['day'] = pd.to_datetime(df1['stamp']).dt.day
#df1.duration = df1.duration / 60

# functionen skal lige nu have to timestaps i vores format.
# Så hvis vi har en god måde at hente dem er det cool.

def TimeDifference(time_1,time_2):
    FMT = '%Y-%m-%d %H:%M:%S'
    tdelta = datetime.strptime(time_1, FMT) - datetime.strptime(time_2, FMT)
    sek_diff = tdelta.days * 24 * 3600 + tdelta.seconds
    return abs(sek_diff)

time_1 = "2021-03-16 17:02:28"
time_2 = "2021-03-18 10:14:55"
sek_diff = TimeDifference(time_1, time_2)



