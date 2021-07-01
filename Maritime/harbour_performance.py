"""
This script is used to calculate the difference in hours for each harbour
"""

import eta2_module as eta
import numpy as np
import pandas as pd


df = eta.get_data_cleaned_eta2()
ports =  df.port.unique().tolist()
n = len(ports)

eta1s = np.zeros(n)
eta2s = np.zeros(n)
stas = np.zeros(n)

for i in range(n):
    eta1s[i], eta2s[i], stas[i] = eta.port_performance(df, ports[i])


row = np.linspace(1,n,n)
data = np.array([[ports],[eta1s/(60*60)],[eta2s/(60*60)],[stas/(60*60)]]).reshape(4, n).T
portdata = pd.DataFrame(data = data, index = row, columns = ["port", "eta1", "eta2", "schedule"])
portdata.dropna(subset = ["eta2"], inplace = "true")
