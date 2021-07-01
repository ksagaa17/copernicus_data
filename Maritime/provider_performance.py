"""
This script is used to calculate the difference in hours 
"""

import eta2_module as eta
import numpy as np
import matplotlib.pyplot as plt


df = eta.get_data_cleaned_eta2()
providers =  df.schedule_source.unique().tolist()

#%% scraper mearsk
sm = providers[0]
sm_mean_eta1, sm_mean_eta2, sm_mean_sta = eta.provider_performance(df, sm)

zoom = 100
n = len(sm_mean_eta1)
plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(n,1,n)
ax.plot(xticks[:zoom], (np.flip(sm_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(sm_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(sm_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.title("Scraper Mearsk")
plt.legend(["eta1","eta2", "schedule"])
plt.savefig("figures/Scraper_Mearsk_{0}.pdf".format(zoom))
plt.show()

#%% scraper one
so = providers[1]
so_mean_eta1, so_mean_eta2, so_mean_sta = eta.provider_performance(df, so)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(n,1,n)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Scraper_One_{0}.pdf".format(zoom))
plt.show()


#%% scraper hapag
sh = providers[2]
sh_mean_eta1, sh_mean_eta2, sh_mean_sta = eta.provider_performance(df, sh)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Scraper_hapag_{0}.pdf".format(zoom))
plt.show()

#%% scraper_anl
sa = providers[3]
sa_mean_eta1, sa_mean_eta2, sa_mean_sta = eta.provider_performance(df, sa)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% scraper_apl
sapl = providers[4]
sapl_mean_eta1, sapl_mean_eta2, sapl_mean_sta = eta.provider_performance(df, sapl)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% scraper_cma
sc = providers[5]
sc_mean_eta1, sc_mean_eta2, sc_mean_sta = eta.provider_performance(df, sc)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% scraper_cnc
scnc = providers[6]
scnc_mean_eta1, scnc_mean_eta2, scnc_mean_sta = eta.provider_performance(df, scnc)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% scraper_sm
ssm = providers[7]
ssm_mean_eta1, ssm_mean_eta2, ssm_mean_sta = eta.provider_performance(df, ssm)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% linscape_MSC
lm = providers[8]
lm_mean_eta1, lm_mean_eta2, lm_mean_sta = eta.provider_performance(df, lm)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% linescape_Zim
lz = providers[9]
lz_mean_eta1, lz_mean_eta2, lz_mean_sta = eta.provider_performance(df, lz)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% linescape_Maersk
lma = providers[10]
lma_mean_eta1, lma_mean_eta2, lma_mean_sta = eta.provider_performance(df, lma)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% Linescape_Hamburg Sud
lh = providers[11]
lh_mean_eta1, lh_mean_eta2, lh_mean_sta = eta.provider_performance(df, lh)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% Linescape_Emirates
le = providers[12]
le_mean_eta1, le_mean_eta2, le_mean_sta = eta.provider_performance(df, le)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% Linescape_Sealand Americas
lsa = providers[13]
lsa_mean_eta1, lsa_mean_eta2, lsa_mean_sta = eta.provider_performance(df, lsa)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(so_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(so_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Scraper One")
plt.savefig("figures/Absolute_difference_eta2_{0}.pdf".format(zoom))
plt.show()

#%% Linescale_WEC lines
lw = providers[14]
lw_mean_eta1, lw_mean_eta2, lw_mean_sta = eta.provider_performance(df, lw)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(lw_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(lw_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(lw_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Linescale_WEC_lines")
plt.savefig("figures/Linescale_WEC_lines{0}.pdf".format(zoom))
plt.show()

#%%Linescale_Unimed
lu = providers[15]
lu_mean_eta1, lu_mean_eta2, lu_mean_sta = eta.provider_performance(df, lu)

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
xticks = np.linspace(393,1,393)
ax.plot(xticks[:zoom], (np.flip(lu_mean_eta1)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(lu_mean_eta2)/(60*60))[:zoom], '-')
ax.plot(xticks[:zoom], (np.flip(lu_mean_sta)/(60*60))[:zoom], '-')
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
plt.legend(["eta1","eta2", "schedule"])
plt.title("Linescale Unimed")
plt.savefig("figures/Linescale_Unimed_{0}.pdf".format(zoom))
plt.show()
