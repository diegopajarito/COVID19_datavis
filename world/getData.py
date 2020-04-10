import pandas as pd
import numpy as np
import requests
import zipfile
import io

# Data source repo: https://github.com/CSSEGISandData
# Mind the changes in data structure for the latest changes
wb_gdp = 'http://api.worldbank.org/v2/en/indicator/NY.GDP.MKTP.CD?downloadformat=csv'
jhu_link_confirmed = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
jhu_link_deaths = 'https://github.com/CSSEGISandData/COVID-19/raw/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
jhu_file_deaths = 'data/time_series_covid19_deaths_global.csv'
jhu_confirmed = ''
jhu_deaths = ''


def get_jhu_confirmed():
    if jhu_confirmed == '':
        # return pd.read_csv('data/time_series_covid19_confirmed_global.csv')
        return pd.read_csv(jhu_link_confirmed)
    else:
        return jhu_confirmed


def get_jhu_deaths():
    if jhu_deaths == '':
        return pd.read_csv(jhu_file_deaths)
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
        countries_data = countries_data.groupby('Country/Region', as_index=False)
        countries_data = countries_data.sum()
        country_names = list(countries_data['Country/Region'])
        countries_data = countries_data.iloc[:, 4:]
        countries_data = countries_data.T
        countries_data = countries_data.reset_index()
        countries_data.columns = ['date'] + country_names
        countries_data['date'] = pd.to_datetime(countries_data['date'])
    return countries_data


def get_confirmed_aggregated():
    jhu_confirmed = get_jhu_confirmed()
    jhu_confirmed = jhu_confirmed.iloc[:, 1:]
    jhu_confirmed = jhu_confirmed.groupby('Country/Region', as_index=False)
    jhu_confirmed = jhu_confirmed.sum()
    return jhu_confirmed


def get_country_deaths(country):
    jhu_deaths = get_jhu_deaths()
    country_data = jhu_deaths[jhu_deaths['Country/Region'] == country]
    if len(country_data) == 1:
        country_data = country_data.iloc[:, 4:]
        country_data = country_data.T
        country_data = country_data.reset_index()
        country_data.columns = ['date', 'deaths']
        country_data['date'] = pd.to_datetime(country_data['date'])
    return country_data


def get_countries_death_rates(countries):
    jhu_confirmed = get_jhu_confirmed()
    jhu_deaths = get_jhu_deaths()
    jhu_confirmed = jhu_confirmed[jhu_confirmed['Country/Region'].isin(countries)]
    jhu_confirmed = jhu_confirmed.groupby('Country/Region', as_index=False)
    jhu_confirmed = jhu_confirmed.sum()
    jhu_deaths = jhu_deaths[jhu_deaths['Country/Region'].isin(countries)]
    jhu_deaths = jhu_deaths.groupby('Country/Region', as_index=False)
    jhu_deaths = jhu_deaths.sum()
    countries_death_rates = jhu_deaths.iloc[:, 4:] / jhu_confirmed.iloc[:, 4:] * 100
    countries_death_rates = countries_death_rates.T
    countries_death_rates = countries_death_rates.reset_index()
    country_names = list(jhu_confirmed['Country/Region'])
    countries_death_rates.columns = ['date'] + countries
    countries_death_rates['date'] = pd.to_datetime(countries_death_rates['date'])
    return countries_death_rates


def get_death_rates():
    jhu_confirmed = get_jhu_confirmed()
    jhu_deaths = get_jhu_deaths()
    last_date = jhu_confirmed.columns[-1]
    death_rates = pd.DataFrame(jhu_confirmed['Province/State'])
    death_rates.columns = ['country']
    death_rates.loc[death_rates['country'].isna(), ['country']] = \
        jhu_confirmed.loc[jhu_confirmed['Province/State'].isna(), 'Country/Region']
    death_rates['days_after_c1'] = 0
    for index, row in jhu_confirmed.iterrows():
        country_data = row[4:]
        country_data = country_data.reset_index()
        country_data.columns = ['day', 'confirmed']
        country_data = country_data[country_data['confirmed'] > 0]
        country_data['day'] = pd.to_datetime(country_data['day'])
        days_after_c1 = country_data['day'].max() - country_data['day'].min()
        death_rates.loc[index, 'days_after_c1'] = days_after_c1/np.timedelta64(1, 'D')
    death_rates['confirmed_cases'] = jhu_confirmed[last_date]
    death_rates['death_cases'] = jhu_deaths[last_date]
    death_rates['death_rate'] = jhu_deaths[last_date] / jhu_confirmed[last_date] * 100
    death_rates = death_rates[death_rates['confirmed_cases'] > 0]
    return death_rates


def get_gdp():
    request = requests.get(wb_gdp)
    zip_file = zipfile.ZipFile(io.BytesIO(request.content))
    gdp = pd.read_csv(zip_file.extract('API_NY.GDP.MKTP.CD_DS2_en_csv_v2_887264.csv'), skiprows=4)
    gdp = gdp[['Country Name', 'Country Code', '2018']]
    gdp.columns = ['country_name', 'country_code', 'gdp_2018']
    return gdp


#data = get_death_rates()
#print (data)