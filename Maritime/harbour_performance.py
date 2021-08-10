"""
This script is used to calculate the difference in hours for each harbour
"""


import eta2_module as eta
import numpy as np
import pandas as pd


file = "eta2_dump"
df = eta.get_data_cleaned_eta2(file)
ports =  df.port.unique().tolist()
n = len(ports)

percent = 0.95
eta1s = np.zeros(n)
eta2s = np.zeros(n)
stas = np.zeros(n)

for i in range(n):
     eta1_tmp, eta2_tmp, sta_tmp = eta.port_performance(df, ports[i], percent)
     eta1s[i] = np.mean(eta1_tmp)
     eta2s[i] = np.mean(eta2_tmp)
     stas[i] = np.mean(sta_tmp)

row = np.linspace(1,n,n)
data = np.array([[ports],[eta1s/(60*60)],[eta2s/(60*60)],[stas/(60*60)]]).reshape(4, n).T

portdata = pd.DataFrame(data = data, index = row, columns = ["port", "eta1", "eta2", "schedule"])

eta2 = portdata['eta2'].to_numpy().astype(str)
nan_eta2 = eta2 != 'nan'
portdata = portdata[nan_eta2]
portdata = portdata.reset_index(drop = True)

#%% plots
ports_counted = df['port'].value_counts()
index = ports_counted.index[:10]

for i in range(len(index)):
    eta1, eta2, sta = eta.port_performance(df, index[i], percent)
    n = len(eta1)
    eta.attribute_plot(eta1, eta2, sta, index[i], n)


# df_CLSAI = df.loc[df["port"]== "CLSAI"]
# df_OMSOH = df.loc[df["port"]== "OMSOH"]

# entries_CLSAI = df_CLSAI.entry_id.unique().tolist()
# entries_OMSOH = df_OMSOH.entry_id.unique().tolist()

# # Interresante
# # 7:MXPGO, 8:SENRK, 11:DECKL, 32:IDJKT, 38:TWKHH, 147:TRMER,

# # Dårlige
# # 2: INTUT, 12:USSAV, KRPUS,
