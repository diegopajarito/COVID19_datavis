import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData


# cumulative curve for a single country
country = 'Italy'
title = 'COVID-19 cases in %s' % country
path = 'plots/deaths_%s' % country
data = getData.get_country_confirmed(country)
data_deaths = getData.get_country_deaths(country)
data = data[data['confirmed_cases'] > 0]
initial_day = data['date'].min()
data['day'] = data['date'] - initial_day
data['day'] = data['day']/np.timedelta64(1, 'D')
data_deaths = data_deaths[data_deaths['deaths'] > 0]
data_deaths['day'] = data_deaths['date'] - initial_day
data_deaths['day'] = data_deaths['day']/np.timedelta64(1, 'D')
ax = sns.lineplot('day', 'confirmed_cases', data=data, label='Confirmed')
ax1 = sns.lineplot('day', 'deaths', data=data_deaths, label='Deaths')
plt.xlabel('Days after first case detected')
plt.ylabel('')
plt.title(title)
plt.savefig(path)
plt.show()
plt.close()


# Death rate curve for multiple countries since case 0
title = 'COVID-19 death cases'
path = 'plots/death_rate_countries'
countries = ['Colombia', 'Mexico', 'Spain', 'Italy', 'US', 'Venezuela', 'Ecuador', 'Peru', 'Brazil']
data_countries = getData.get_countries_death_rates(countries)
countries = data_countries.columns
for country in countries[1:]:
    data_country = data_countries.loc[:, ['date', country]]
    ax = sns.lineplot(x='date', y=country, data=data_country.dropna(), label=country)
plt.title('COVID-19 Death Rates')
plt.ylabel('Death Rates (%)')
plt.xticks(rotation=45, size=6)
plt.savefig(path)
plt.close()


death_rates = getData.get_death_rates()
sns.distplot(death_rates.iloc[:208, 'death_rate'])
sns.distplot(death_rates.iloc[:208, 2])
sns.boxplot(death_rates.iloc[:208, 2])
