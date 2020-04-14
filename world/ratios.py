import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData


# Death rate curve for multiple countries since case 0
title = 'COVID-19 death / conformed cases'
path = 'plots/death_rate_countries'
countries = ['China', 'France', 'Germany', 'Italy', 'Iran',  'Spain', 'Switzerland', 'Turkey', 'United Kingdom', 'US']
# countries = ['Colombia', 'Mexico', 'Spain', 'Italy', 'US', 'Venezuela', 'Ecuador', 'Peru', 'Brazil']
data_countries = getData.get_countries_death_rates(countries)
countries = data_countries.columns
for country in countries[1:]:
    data_country = data_countries.loc[:, ['date', country]]
    ax = sns.lineplot(x='date', y=country, data=data_country.dropna(), label=country)
plt.title('COVID-19 Death Rates')
plt.ylabel('Death Rates (%)')
plt.ylim(0, 13)
plt.xticks(rotation=45, size=6)
plt.savefig(path)
plt.close()


# Death cases Vs. Death Rate
death_rates = getData.get_death_rates()
sns.scatterplot(x='days_after_c1', y='death_rate', hue='death_cases', size='death_cases', data=death_rates)
plt.xlabel('Days after Case 1')
plt.ylabel('Death Rate % (Deaths/Confirmed)')
plt.savefig('plots/deaths_rates_days.png')

sns.distplot(death_rates['death_rate'])
sns.scatterplot('days_after_c1', 'death_rate', data=death_rates)
sns.scatterplot('confirmed_cases', 'death_rate', data=death_rates, size=0.3, alpha=0.7, legend=False)


sns.scatterplot('days_after_c1', 'death_rate', data=death_rates, size=0.3, alpha=0.7, legend=False)


sns.scatterplot('confirmed_cases', 'death_rate', data=death_rates[death_rates['confirmed_cases'] > 500], size=0.3, alpha=0.7, legend=False)



ax = sns.scatterplot('confirmed_cases', 'death_rate', data=death_rates[death_rates['confirmed_cases'] > 1000], size='death_cases', alpha=0.6)
ax.set(xscale='log')


sns.scatterplot('death_cases', 'death_rate', data=death_rates[death_rates['death_cases'] > 30], size='confirmed_cases', alpha=0.6)