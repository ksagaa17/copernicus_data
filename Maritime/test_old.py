import numpy as np
import utillities as ut



month = 1
df = ut.get_data(1)

track_ids = df.track_id.unique()
hours_bef_arrive = np.zeros(0)
for track_id in track_ids:
    df_small = df.loc[df['track_id']==track_id]
    stamp = df_small['stamp'].to_numpy().astype('datetime64[s]')
    ata = ut.ata_Extract(df, track_id, status = 14).astype('datetime64[s]')
    diff = (ata[:1] - stamp).astype('timedelta64[h]')
    hours_bef_arrive = np.concatenate((hours_bef_arrive,diff.astype(int)))
    
df['hours_bef_arr'] = hours_bef_arrive

