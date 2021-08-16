"""
Creates dataframe showing the performance of the different providers
"""


import pandas as pd
import numpy as np
import eta2_module as eta


file = "eta2_dump"
df = eta.get_data_cleaned_eta2(file)
df_small = eta.nextport_dataframe(file)
providers =  df.schedule_source.unique().tolist()
percent = 0.90

m = len(providers)

eta1s = np.zeros(m)
eta2s = np.zeros(m)
stas = np.zeros(m)
nports = np.zeros(m)
# points = np.zeros(m)

for i in range(m):
    eta1_tmp, eta2_tmp, sta_tmp = eta.provider_performance(df, providers[i], percent)
    nport_tmp = eta.provider_performance_nextport(df_small, providers[i], percent)
    eta1s[i] = np.mean(eta1_tmp)
    eta2s[i] = np.mean(eta2_tmp)
    stas[i] = np.mean(sta_tmp) 
    nports[i] = np.mean(nport_tmp)
    # if type(eta1_tmp) != int:
    #     points[i] = len(eta1_tmp)

divider = 60*60
row = np.linspace(1,m,m)
data = np.array([[providers],[eta1s/(divider)],[eta2s/(divider)],[stas/(divider)], [nports/(divider)]]).reshape(5, m).T

providerdata = pd.DataFrame(data = data, index = row,
                            columns = ["provider", "eta1", "eta2", "schedule", "nextport_eta"])

eta2 = providerdata['eta2'].to_numpy().astype(str)
nan_eta2 = eta2 != 'nan'
providerdata = providerdata[nan_eta2]
providerdata = providerdata.reset_index(drop = True)

#%% plots
providers_counted = df['schedule_source'].value_counts()
index = providers_counted.index[:8]

for i in range(len(index)):
    eta1, eta2, sta = eta.provider_performance(df, index[i], percent)
    nport = eta.provider_performance_nextport(df_small, index[i], percent)
    n = len(eta1)
    m = len(nport)
    eta.attribute_plot(eta1, eta2, sta, nport, index[i], 250, 250)
