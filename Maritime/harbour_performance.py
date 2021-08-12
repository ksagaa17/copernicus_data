"""
This script is used to calculate the difference in hours for each harbour
"""


import eta2_module as eta
import numpy as np
import pandas as pd


file = "eta2_dump"
df = eta.get_data_cleaned_eta2(file)
df_small = eta.nextport_dataframe(file)
ports =  df.port.unique().tolist()
n = len(ports)

percent = 0.95
eta1s = np.zeros(n)
eta2s = np.zeros(n)
stas = np.zeros(n)
nports = np.zeros(n)

for i in range(n):
     eta1_tmp, eta2_tmp, sta_tmp = eta.port_performance(df, ports[i], percent)
     nport_tmp = eta.port_performance_nextport(df_small, ports[i], percent)
     eta1s[i] = np.mean(eta1_tmp)
     eta2s[i] = np.mean(eta2_tmp)
     stas[i] = np.mean(sta_tmp)
     #if nport_tmp != False:
     nports[i] = np.mean(nport_tmp)

divider = 60*60
row = np.linspace(1,n,n)
data = np.array([[ports],[eta1s/(divider)],[eta2s/(divider)],[stas/(divider)], [nports/(divider)]]).reshape(5, n).T
portdata = pd.DataFrame(data = data, index = row, columns = ["port", "eta1", "eta2", "schedule", "nextport"])

eta2 = portdata['eta2'].to_numpy().astype(str)
nan_eta2 = eta2 != 'nan'
portdata = portdata[nan_eta2]
portdata = portdata.reset_index(drop = True)

#%% plots
ports_counted = df['port'].value_counts()
index = ports_counted.index[:10]

for i in range(len(index)):
    eta1, eta2, sta = eta.port_performance(df, index[i], percent)
    nport = eta.port_performance_nextport(df_small, index[i], percent)
    n = len(eta1)
    m = len(nport)
    eta.attribute_plot(eta1, eta2, sta, nport, index[i], n, m)


# df_CLSAI = df.loc[df["port"]== "CLSAI"]
# df_OMSOH = df.loc[df["port"]== "OMSOH"]

# entries_CLSAI = df_CLSAI.entry_id.unique().tolist()
# entries_OMSOH = df_OMSOH.entry_id.unique().tolist()

# # Interresante
# # 7:MXPGO, 8:SENRK, 11:DECKL, 32:IDJKT, 38:TWKHH, 147:TRMER,

# # Dårlige
# # 2: INTUT, 12:USSAV, KRPUS,
