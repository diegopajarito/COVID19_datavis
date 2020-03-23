import pandas as pd
import urllib.request
ins_co_link = "https://e.infogram.com/3a4c9dd3-fbb8-4f59-8d82-eb1edc01604b?src=embed#"
ins_co_file = 'data/Casos.csv'
names = ['id_case', 'date', 'city', 'region', 'treatment', 'age', 'sex', 'origin', 'origin_country']


def get_ins_data():
    ins_co_data = pd.read_csv(ins_co_link)
    return ins_co_data


def get_ins_data_file():
    ins_co_data = pd.read_csv(ins_co_file)
    ins_co_data.columns = names
    ins_co_data['date'] = pd.to_datetime(ins_co_data['date'])
    return ins_co_data

