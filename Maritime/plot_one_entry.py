"""
This script is used to plot a single entry as to see how a given ship behaves.
"""


import eta2_module as eta


df = eta.get_data_cleaned_eta2()
#df_small = df.loc[df["port"] == "IDJKT"]
df_small = df.loc[df["schedule_source"] == "linescape_Zim"]
df_small = df_small.reset_index(drop=True)
entries = df_small.entry_id.unique().tolist()

#%%
for i in range(len(entries)):
    eta.plot_eta_entry(df_small, entries[i])
