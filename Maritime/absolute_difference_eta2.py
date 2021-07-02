"""
This scripts is used to calculate the absolute difference in time of arrival
for the eta1 and eta2 algorithm and the scheduled arrival. 
"""


import matplotlib.pyplot as plt
import eta2_module as eta
import numpy as np


df = eta.get_data_cleaned_eta2()
mean_eta1, mean_eta2, mean_sta = eta.absolute_difference(df)
n = len(mean_eta1)
zoom = 200

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(1,n,n)
ax.plot(xticks[:zoom], mean_eta1[:zoom]/(60*60))
ax.plot(xticks[:zoom], mean_eta2[:zoom]/(60*60))
ax.plot(xticks[:zoom], mean_sta[:zoom]/(60*60))
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()
