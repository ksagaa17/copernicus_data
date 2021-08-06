"""
This scripts is used to calculate the absolute difference in time of arrival
for the eta1 and eta2 algorithm and the scheduled arrival. 
"""


import matplotlib.pyplot as plt
import eta2_module as eta
import numpy as np


file = "eta2_dump.csv"
df = eta.get_data_cleaned_eta2(file)
percent = 0.9
mean_sta = eta.absolute_difference_sta(df, percent)
mean_eta1 = eta.absolute_difference_eta1(df, percent)
mean_eta2 = eta.absolute_difference_eta2(df, percent)
mean_nport = eta.absolute_difference_nextport(df, percent)


divider = 60*60



final_mean_eta1 = np.mean(mean_eta1)/divider
final_mean_eat2 = np.mean(mean_eta2)/divider
final_mean_sta = np.mean(mean_sta)/divider
final_mean_nport = np.mean(mean_nport)/divider

#%% plotting

n = len(mean_eta1)
zoom = 200 #n 

m = len(mean_nport)
zoom2 = 200 #m

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(1,n,n)
xticks2 = np.linspace(1,m,m)
ax.plot(xticks[:zoom], mean_eta1[:zoom]/divider)
ax.plot(xticks[:zoom], mean_eta2[:zoom]/divider)
ax.plot(xticks[:zoom], mean_sta[:zoom]/divider)
ax.plot(xticks2[:zoom2], mean_nport[:zoom2]/divider)

ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule", "nextport"])
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()
