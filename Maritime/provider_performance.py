"""
This script is used to calculate the difference in hours for each provider
"""


import eta2_module as eta
import numpy as np
import matplotlib.pyplot as plt


df = eta.get_data_cleaned_eta2()
providers =  df.schedule_source.unique().tolist()

#%% Scraper mearsk
sm = providers[0]
sm_mean_eta1, sm_mean_eta2, sm_mean_sta = eta.provider_performance(df, sm)
n = len(sm_mean_eta1)
eta.provider_plot(sm_mean_eta1, sm_mean_eta2, sm_mean_sta, "Scraper_Mearsk", n)

#%% Scraper one
so = providers[1]
so_mean_eta1, so_mean_eta2, so_mean_sta = eta.provider_performance(df, so)
n = len(so_mean_eta1)
eta.provider_plot(so_mean_eta1, so_mean_eta2, so_mean_sta, "Scraper_One", n)

#%% Scraper cosco
scos = providers[2]
scos_mean_eta1, scos_mean_eta2, scos_mean_sta = eta.provider_performance(df, scos)
n = len(scos_mean_eta1)
eta.provider_plot(scos_mean_eta1, scos_mean_eta2, scos_mean_sta, "Scraper_Cosco", n)

#%% Scraper hapag
sh = providers[3]
sh_mean_eta1, sh_mean_eta2, sh_mean_sta = eta.provider_performance(df, sh)
n = len(sh_mean_eta1)
eta.provider_plot(sh_mean_eta1, sh_mean_eta2, sh_mean_sta, "Scraper_Hapag", n)

#%% Scraper_anl
sa = providers[4]
sa_mean_eta1, sa_mean_eta2, sa_mean_sta = eta.provider_performance(df, sa)
n = len(sa_mean_eta1)
eta.provider_plot(sa_mean_eta1, sa_mean_eta2, sa_mean_sta, "Scraper_ANL", n)

#%% Scraper_apl
sapl = providers[5]
sapl_mean_eta1, sapl_mean_eta2, sapl_mean_sta = eta.provider_performance(df, sapl)
n = len(sapl_mean_eta1)
eta.provider_plot(sapl_mean_eta1, sapl_mean_eta2, sapl_mean_sta, "Scraper_APL", n)

#%% Scraper_cma
sc = providers[6]
sc_mean_eta1, sc_mean_eta2, sc_mean_sta = eta.provider_performance(df, sc)
n = len(sc_mean_eta1)
eta.provider_plot(sc_mean_eta1, sc_mean_eta2, sc_mean_sta, "Scraper_CMA", n)

#%% Scraper_cnc
scnc = providers[7]
scnc_mean_eta1, scnc_mean_eta2, scnc_mean_sta = eta.provider_performance(df, scnc)
n = len(scnc_mean_eta1)
eta.provider_plot(scnc_mean_eta1, scnc_mean_eta2, scnc_mean_sta, "Scraper_CNC", n)

#%% Scraper_SM
ssm = providers[8]
ssm_mean_eta1, ssm_mean_eta2, ssm_mean_sta = eta.provider_performance(df, ssm)
n = len(ssm_mean_eta1)
eta.provider_plot(ssm_mean_eta1, ssm_mean_eta2, ssm_mean_sta, "Scraper_SM", n)

#%% Linscape_MSC
lm = providers[9]
lm_mean_eta1, lm_mean_eta2, lm_mean_sta = eta.provider_performance(df, lm)
n = len(lm_mean_eta1)
eta.provider_plot(lm_mean_eta1, lm_mean_eta2, lm_mean_sta, "Linescape_MSC", n)

#%% Linescape_Zim
lz = providers[10]
lz_mean_eta1, lz_mean_eta2, lz_mean_sta = eta.provider_performance(df, lz)
n = len(lz_mean_eta1)
eta.provider_plot(lz_mean_eta1, lz_mean_eta2, lz_mean_sta, "Linescape_Zim", n)

#%% Linescape_Maersk
lma = providers[11]
lma_mean_eta1, lma_mean_eta2, lma_mean_sta = eta.provider_performance(df, lma)
n = len(lma_mean_eta1)
eta.provider_plot(lma_mean_eta1, lma_mean_eta2, lma_mean_sta, "Linescape_Maersk", n)

#%% Linescape_Hamburg Sud
lh = providers[12]
lh_mean_eta1, lh_mean_eta2, lh_mean_sta = eta.provider_performance(df, lh)
n = len(lh_mean_eta1)
eta.provider_plot(lh_mean_eta1, lh_mean_eta2, lh_mean_sta, "Linescape_Hamburg_Sud", n)

#%% Linescape_Emirates
le = providers[13]
le_mean_eta1, le_mean_eta2, le_mean_sta = eta.provider_performance(df, le)
n = len(le_mean_eta1)
eta.provider_plot(le_mean_eta1, le_mean_eta2, le_mean_sta, "Linescape_Emirates", n)

#%% Linescape_Sealand Americas
lsa = providers[14]
lsa_mean_eta1, lsa_mean_eta2, lsa_mean_sta = eta.provider_performance(df, lsa)
n = len(lsa_mean_eta1)
eta.provider_plot(lsa_mean_eta1, lsa_mean_eta2, lsa_mean_sta, "Linescape_Sealand_Americas", n)

#%% Linescale_WEC lines
lw = providers[15]
lw_mean_eta1, lw_mean_eta2, lw_mean_sta = eta.provider_performance(df, lw)
n = len(lw_mean_eta1)
eta.provider_plot(lw_mean_eta1, lw_mean_eta2, lw_mean_sta, "Linescale_WEC_Lines", n)

#%% Linescale_Unimed
lu = providers[16]
lu_mean_eta1, lu_mean_eta2, lu_mean_sta = eta.provider_performance(df, lu)
n = len(lu_mean_eta1)
eta.provider_plot(lu_mean_eta1, lu_mean_eta2, lu_mean_sta, "Linescale_Unimed", n)

#%% Combined plot

plt.style.use('seaborn-darkgrid')
fig, ax = plt.subplots()
ax.plot(np.linspace(1,len(sm_mean_eta2),len(sm_mean_eta2)), sm_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(so_mean_eta2),len(so_mean_eta2)), so_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(scos_mean_eta2),len(scos_mean_eta2)), scos_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(sh_mean_eta2),len(sh_mean_eta2)), sh_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(sa_mean_eta2),len(sa_mean_eta2)), sa_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(sapl_mean_eta2),len(sapl_mean_eta2)), sapl_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(sc_mean_eta2),len(sc_mean_eta2)), sc_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(scnc_mean_eta2),len(scnc_mean_eta2)), scnc_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(ssm_mean_eta2),len(ssm_mean_eta2)), ssm_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(lm_mean_eta2),len(lm_mean_eta2)), lm_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(lz_mean_eta2),len(lz_mean_eta2)), lz_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(lma_mean_eta2),len(lma_mean_eta2)), lma_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(lh_mean_eta2),len(lh_mean_eta2)), lh_mean_eta2/(60*60))
#ax.plot(np.linspace(1,len(le_mean_eta2),len(le_mean_eta2)), le_mean_eta2/(60*60))
ax.plot(np.linspace(1,len(lsa_mean_eta2),len(lsa_mean_eta2)), lsa_mean_eta2/(60*60))
#ax.plot(np.linspace(1,len(lw_mean_eta2),len(lw_mean_eta2)), lw_mean_eta2/(60*60))
#ax.plot(np.linspace(1,len(lu_mean_eta2),len(lu_mean_eta2)), lu_mean_eta2/(60*60))
ax.invert_xaxis()
ax.set_ylabel("Absolute error in hours")
ax.set_xlabel('Hours before arrival')
# plt.legend(["Scraper Mearsk","Scraper One", "Scraper Cosco", "Scraper Hapag", "Scraper ANL", "Scraper APL",
#             "Scraper CMA", "Scraper CNC", "Scraper SM", "Linescape MSC", "Linescape Zim", "Linescape Maersk",
#             "Linescape Hamburg Sud", "Linescape Emirates", "Linescape Sealand Americas", "Linescape WEC Lines",
#             "Linescape Unimed"])
plt.legend(loc = "upper right", bbox_to_anchor = (1.51,1), labels = ["Scraper Mearsk","Scraper One", "Scraper Cosco", "Scraper Hapag", "Scraper ANL", "Scraper APL",
             "Scraper CMA", "Scraper CNC", "Scraper SM", "Linescape MSC", "Linescape Zim", "Linescape Maersk",
             "Linescape Hamburg Sud", "Linescape Sealand Americas"])
plt.title("ETA2 comparison")
plt.savefig("figures/Provider_comparison.pdf")
plt.show()
