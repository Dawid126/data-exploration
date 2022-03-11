import psycopg2
import sqlalchemy
import requests
from datetime import timedelta
import configparser
import pandas as pd

def set_database_connection(config):
    url = 'postgresql+psycopg2://' + config.get('database', 'user') + ':' + config.get('database', 'password') + '@' \
          + config.get('database', 'host') + ':' + config.get('database', 'port') + '/postgres'
    return sqlalchemy.create_engine(url)

def get_data_to_save(request_result):
    columns = {
        "id_stacji": "STATION_ID", 
        "stacja": "STATION_NAME", 
        "temperatura": "TEMPERATURE", 
        "predkosc_wiatru": "WIND_VELOCITY",
        "kierunek_wiatru": "WIND_DIRECTION",
        "wilgotnosc_wzgledna": "HUMIDITY",
        "suma_opadu": "TOTAL_PRECIPITATION",
        "cisnienie": "PRESSURE",
        "data_pomiaru": "DATE",
        "godzina_pomiaru": "HOUR"
    }
    columns_types = {
        "STATION_ID": "int64",
        "STATION_NAME": "string",
        "DATE": "datetime64",
        "HOUR": "int64",
        "TEMPERATURE": "float64",
        "WIND_VELOCITY": "float64",
        "WIND_DIRECTION": "float64",
        "HUMIDITY": "float64",
        "TOTAL_PRECIPITATION": "float64",
        "PRESSURE": "float64"
    }
    weather_data = pd.json_normalize(request_result).rename(columns=columns).astype(columns_types)
    weather_data["DATE"] = weather_data["DATE"] + weather_data["HOUR"].apply(lambda x: timedelta(hours=x))
    weather_data = weather_data.drop(columns=["HOUR"])
    return weather_data
    

url = "https://danepubliczne.imgw.pl/api/data/synop/station/krakow"
headers = {'Accept': 'application/json'}
request_result = requests.get(url, headers=headers).json()
weather_history_data_frame = get_data_to_save(request_result)

config = configparser.ConfigParser()
config.read('properties.properties')
connection = set_database_connection(config)
weather_history_data_frame.to_sql('WEATHER_HISTORY_DATA_IMGW', connection, schema='public', if_exists='append', index=False)