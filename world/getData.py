import pandas as pd
import urllib.request

# Data source repo: https://github.com/CSSEGISandData
# Mind the changes in data structure for the latest changes
jhu_link_confirmed = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
jhu_link_death = 'https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
jhu_confirmed = ''
jhu_death = ''


def get_jhu_confirmed():
    if jhu_confirmed == '':
        return pd.read_csv('data/time_series_covid19_confirmed_global.csv')
        # return pd.read_csv(jhu_link_confirmed)
    else:
        return jhu_confirmed


def get_jhu_dead():
    if jhu_death == '':
        return pd.read_csv(jhu_link_death)
    else:
        return jhu_confirmed


def get_country_confirmed(country):
    jhu_confirmed = get_jhu_confirmed()
    country_data = jhu_confirmed[jhu_confirmed['Country/Region'] == country]
    if len(country_data) == 1:
        country_data = country_data.iloc[:, 4:]
        country_data = country_data.T
        country_data = country_data.reset_index()
        country_data.columns = ['date', 'confirmed_cases']
        country_data['date'] = pd.to_datetime(country_data['date'])
    return country_data


def get_countries_confirmed(countries):
    jhu_confirmed = get_jhu_confirmed()
    countries_data = jhu_confirmed[jhu_confirmed['Country/Region'].isin(countries)]
    if len(countries_data) > 0:
        country_names = list(countries_data['Country/Region'])
        countries_data = countries_data.iloc[:, 4:]
        countries_data = countries_data.T
        countries_data = countries_data.reset_index()
        countries_data.columns = ['date'] + country_names
        countries_data['date'] = pd.to_datetime(countries_data['date'])
    return countries_data


data = get_countries_confirmed(['Colombia', 'Spain'])
print (data)