import psycopg2
import configparser
import requests
import pandas as pd
import numpy as np
import sqlalchemy

def flatten(data):
    return sum(data, [])


def extract_values(data, type):
    return list(map(lambda x: x[type], data))


def filter_value(data, type):
    return filter(lambda x: x['name'] == type, data)


def set_database_connection(config):
    url = 'postgresql+psycopg2://' + config.get('database', 'user') + ':' + config.get('database', 'password') + '@' \
          + config.get('database', 'host') + ':' + config.get('database', 'port') + '/postgres'
    return sqlalchemy.create_engine(url=url)


def get_data_to_save(sensors, measurements_url, headers):
    pollutants_history_data_frames = []
    # pollutants_forecast_data_frames = []
    weather_history_data_frames = []

    for sensor_name, sensor_id, inner in sensors.values:
        url = measurements_url + str(sensor_id)
        print("Requesting data for {}".format(sensor_name))
        response = requests.get(url, headers=headers).json()


        history = response['history']
        history_values = flatten(extract_values(history, 'values'))
        pollutants_history_data = {pollutant: extract_values(filter_value(history_values, pollutant), 'value')
                                   for pollutant in pollutants_params}

        pollutants_history_data_frame = pd.DataFrame(data={'SENSOR_ID': np.full(len(history), sensor_id),
                                                           'DATE': extract_values(history, 'fromDateTime'),
                                                           'INNER': inner,
                                                           **pollutants_history_data})
        pollutants_history_data_frames.append(pollutants_history_data_frame)

        # forecast = response['forecast']
        # forecast_values = flatten(extract_values(forecast, 'values'))
        # forecast_pollutants_data = {pollutant: extract_values(filter_value(forecast_values, pollutant), 'value')
        #                             for pollutant in pollutants_params}
        # pollutants_forecast_data_frame = pd.DataFrame(data={'Sensor_ID': np.full(len(forecast), sensor_id),
        #                                                     'Date': extract_values(forecast, 'fromDateTime'),
        #                                                     **forecast_pollutants_data})
        # pollutants_forecast_data_frames.append(pollutants_forecast_data_frame)

        weather_history_data = {weather_param: extract_values(filter_value(history_values, weather_param), 'value')
                                for weather_param in weather_params}

        weather_history_data_frame = pd.DataFrame(data={'SENSOR_ID': np.full(len(history), sensor_id),
                                                        'DATE': extract_values(history, 'fromDateTime'),
                                                        'INNER': inner,
                                                        **weather_history_data})

        weather_history_data_frames.append(weather_history_data_frame)

    return pollutants_history_data_frames, weather_history_data_frames


config = configparser.ConfigParser()
config.read('properties.properties')

measurements_url = 'https://airapi.airly.eu/v2/measurements/installation?installationId='
headers = {'apikey': config.get('airly', 'api_key'),
           'Accept': 'application/json'}

sensors = pd.read_csv('sensors.csv', sep=';')
pollutants_params = ['PM1', 'PM25', 'PM10']
weather_params = ['TEMPERATURE', 'HUMIDITY', 'PRESSURE']

connection = set_database_connection(config)
pollutants_history_data_frames, weather_history_data_frames = get_data_to_save(sensors, measurements_url, headers)

for (pollutant_data_frame, weather_data_frame) in zip(pollutants_history_data_frames, weather_history_data_frames):
    pollutant_data_frame.to_sql('POLLUTANTS_HISTORY_DATA', connection, schema='public', if_exists='append', index=False)
    weather_data_frame.to_sql('WEATHER_HISTORY_DATA_AIRLY', connection, schema='public', if_exists='append', index=False)

