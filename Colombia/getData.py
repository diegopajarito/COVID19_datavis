import pandas as pd
import urllib.request
ins_co_link = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
ins_co_file = 'data/Casos.csv'
names = ['id_case', 'date', 'city', 'region', 'treatment', 'age', 'sex', 'origin', 'origin_country', 'date_death',
         'date_recovered']


def get_ins_data():
    ins_co_data = pd.read_csv(ins_co_link)
    return ins_co_data


def get_ins_data_file():
    ins_co_data = pd.read_csv(ins_co_file)
    ins_co_data.columns = names
    ins_co_data['date_str'] = ins_co_data['date']
    ins_co_data['date'] = pd.to_datetime(ins_co_data['date'], dayfirst=True, errors='coerce')
    return ins_co_data

