import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import getData

# Colombia and Neighbourhoods, Latin / South America, Top World Col, Europe.
groups = [['Europe', 'Europe.png',
           ['Portugal', 'Spain', 'Italy', 'France', 'Germany', 'Belgium', 'Netherlands', 'Denmark',  'Andorra', 'Croatia'
            'Greece', 'Ireland', 'Sweden', 'Poland', 'Czech Republic', 'Austria', 'Hungary', 'Romania', 'Bulgaria']],
          ['Colombia and Neighbourhood Countries', 'co_neighbourhood.png',
           ['Colombia', 'Venezuela', 'Ecuador', 'Panama', 'Brazil', 'Bolivia', 'Peru']],
          ['South America', 'co_latin_america.png',
           ['Colombia', 'Venezuela', 'Ecuador', 'Peru', 'Bolivia', 'Chile', 'Brazil', 'Argentina', 'Paraguay', 'Uruguay', 'Guyana']],
          ['Top 10 Countries', 'top_10.png',
           ['US', 'Spain', 'Italy', 'Germany', 'France', 'China', 'Iran', 'United Kingdom', 'Turkey', 'Switzerland']]]

for group in groups:
    title = group[0]
    path = group[1]
    countries = group[2]
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
    plt.title('COVID-19 Confirmed Cases - %s' % title)
    plt.ylabel('Confirmed Cases (log)')
    plt.xlabel('Days after case zero')
    plt.show()
    plt.savefig('plots/%s' % path)
    plt.close()
