# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 17:06:26 2021

"""

import pandas as pd
import numpy as np

df = pd.read_csv("data/tbl_ship_arrivals_log_202103.log", sep = "|", header=None)
df.columns = ['track_id', 'mmsi', 'status', 'port_id', 'shape_id', 'stamp',
              'eta_erp', 'eta_ais', 'ata_ais', 'bs_ts', 'sog', 'username']

df = df.sort_values(by=['track_id'])
track_id = df['track_id'].to_numpy()
number_of_ids = len(np.unique(track_id))

status = df['status'].to_numpy()
arrivals = np.sum(status == 14)

df_arrive = df.loc[df['status'] == 14]

df_small = df.loc[df['track_id'].isin(df_arrive['track_id'])]

df_eta = df_small.loc[df_small['status'] != 14]

df_final = df_small.loc[df_small['track_id'].isin(df_eta['track_id'])]


# Vi vil i sidste ende gerne kunne regne mean(|eta - ata|)

# parametre vi vil teste

# eta1
# givet et skib og hvor det er på vej hen

# det beregner en rute og givet nogle historiske hastigheder beregnes en eta.

# Givet en log hvor godt rammer vi tidspunktet

# 90 % bedste bud hvor godt rammer vi ata, 

# Hvor godt performer vi for erp_eta.


# eta2
# Containerskibe - kan lave eta på en hele rute

# destination predictor
