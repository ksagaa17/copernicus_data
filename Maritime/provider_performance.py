"""
Creates dataframe showing the performance of the different providers
"""


import pandas as pd
import numpy as np
import eta2_module as eta


df = eta.get_data_cleaned_eta2()
providers =  df.schedule_source.unique().tolist()

m = len(providers)

eta1s = np.zeros(m)
eta2s = np.zeros(m)
stas = np.zeros(m)

for i in range(m):
    eta1_tmp, eta2_tmp, sta_tmp = eta.provider_performance(df, providers[i])
    eta1s[i] = np.mean(eta1_tmp)
    eta2s[i] = np.mean(eta2_tmp)
    stas[i] = np.mean(sta_tmp) 

row = np.linspace(1,m,m)
data = np.array([[providers],[eta1s/(60*60)],[eta2s/(60*60)],[stas/(60*60)]]).reshape(4, m).T

providerdata = pd.DataFrame(data = data, index = row,
                            columns = ["provider", "eta1", "eta2", "schedule"])

eta2 = providerdata['eta2'].to_numpy().astype(str)
nan_eta2 = eta2 != 'nan'
providerdata = providerdata[nan_eta2]
providerdata = providerdata.reset_index(drop = True)
