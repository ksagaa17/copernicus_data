"""
This script is used to calculate the difference in hours for each provider
"""


import eta2_module as eta



df = eta.get_data_cleaned_eta2()
providers =  df.schedule_source.unique().tolist()
provider_counted = df['schedule_source'].value_counts()
index = provider_counted.index[:10]
m = len(providers)

for i in range(m):
    eta1, eta2, sta = eta.provider_performance(df, providers[i])
    n = len(eta1)
    eta.attribute_plot(eta1, eta2, sta, providers[i], n)
