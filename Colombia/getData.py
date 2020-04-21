import pandas as pd
import urllib.request
ins_co_link = "https://www.datos.gov.co/api/views/gt2j-8ykr/rows.csv?accessType=DOWNLOAD"
ins_co_file = 'data/Casos.csv'
names = ['id_case', 'date_notification', 'divipola', 'city', 'region', 'treatment', 'age', 'sex', 'origin', 'state',
         'origin_country', 'fis', 'date_death', 'data_diagnostic', 'date_recovered', 'date_web']


def get_ins_data():
    ins_co_data = pd.read_csv(ins_co_link)
    ins_co_data.to_csv(ins_co_file)
    ins_co_data.columns = names
    ins_co_data['date_str'] = ins_co_data['fis']
    ins_co_data['fis'] = pd.to_datetime(ins_co_data['fis'], dayfirst=True, errors='coerce')
    ins_co_data['date_notification'] = pd.to_datetime(ins_co_data['date_notification'], dayfirst=True, errors='coerce')
    ins_co_data['date_death'] = pd.to_datetime(ins_co_data['date_death'], dayfirst=True, errors='coerce')
    ins_co_data['data_diagnostic'] = pd.to_datetime(ins_co_data['data_diagnostic'], dayfirst=True, errors='coerce')
    ins_co_data['date_recovered'] = pd.to_datetime(ins_co_data['date_recovered'], dayfirst=True, errors='coerce')
    ins_co_data['divipola'] = pd.to_numeric(ins_co_data['divipola'], downcast='integer')
    return ins_co_data


def get_ins_data_file():
    ins_co_data = pd.read_csv(ins_co_file)
    ins_co_data.columns = names
    ins_co_data['date_str'] = ins_co_data['fis']
    ins_co_data['fis'] = pd.to_datetime(ins_co_data['fis'], dayfirst=True, errors='coerce')
    ins_co_data['date_notification'] = pd.to_datetime(ins_co_data['date_notification'], dayfirst=True, errors='coerce')
    ins_co_data['date_death'] = pd.to_datetime(ins_co_data['date_death'], dayfirst=True, errors='coerce')
    ins_co_data['data_diagnostic'] = pd.to_datetime(ins_co_data['data_diagnostic'], dayfirst=True, errors='coerce')
    ins_co_data['date_recovered'] = pd.to_datetime(ins_co_data['date_recovered'], dayfirst=True, errors='coerce')
    ins_co_data['divopola'] = int(ins_co_data['divopola'])
    return ins_co_data

