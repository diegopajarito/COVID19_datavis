import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData


# cumulative curve for a single country
country = 'Italy'
title = 'COVID-19 %s' % country
path = 'plots/cases_%s' % country
data = getData.get_country_confirmed(country)
data = data[data['confirmed_cases'] > 0]
initial_day = data['date'].min()
data['day'] = data['date'] - initial_day
data['day'] = data['day']/np.timedelta64(1, 'D')
ax = sns.lineplot('day', 'confirmed_cases', data=data)
ax.set(xlabel='Days after first case detected', ylabel='Confirmed cases', title=title)
plt.savefig(path)
plt.show()
plt.close()

# cumulative curve for multiple countries
title = 'COVID-19 confirmed cases'
path = 'plots/cases_countries'
countries = ['Colombia', 'Mexico', 'Spain', 'Italy', 'US']
data_countries = getData.get_countries_confirmed(countries)
countries = data_countries.columns
for country in countries[1:]:
    ax = sns.lineplot(x='date', y=country, data=data_countries, label=country)
ax.set(yscale="log")
plt.xticks(rotation=45, size=6)
plt.title('COVID-19 Confirmed Cases')
plt.ylabel('Confirmed Cases (log)')
plt.xlabel('')
plt.savefig('plots/confirmed_cases_date.png')
plt.close()



# cumulative curve for multiple countries in days since case 0
title = 'COVID-19 confirmed cases'
path = 'plots/cases_countries'
countries = ['Colombia', 'Mexico', 'Spain', 'Italy', 'US', 'Ecuador', 'Peru', 'Brazil']
data_countries = getData.get_countries_confirmed(countries)
countries = data_countries.columns
for country in countries[1:]:
    data_country = data_countries.loc[:, ['date', country]]
    data_country = data_country[data_country[country] > 1]
    initial_day = data_country['date'].min()
    data_country['day'] = data_country['date'] - initial_day
    data_country['day'] = data_country['day'] / np.timedelta64(1, 'D')
    ax = sns.lineplot(x='day', y=country, data=data_country, label=country)
ax.set(yscale="log")
plt.title('COVID-19 Confirmed Cases')
plt.ylabel('Confirmed Cases (log)')
plt.xlabel('Days after case zero')
plt.savefig('plots/confirmed_cases_days.png')
plt.close()


