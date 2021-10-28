import requests
from datetime import datetime, timedelta
import pandas as pd
import vincent
import json
from tqdm import tqdm

WATER_LEVEL_API = '{city_name}/history?time={time_stamp}'
TIMEFORMAT = "%Y-%m-%d-%H-%M-%S"
CITIES = ["tvlongdinh", "tvmytho"]
DATABASE = './data/database/db.csv'

class MyAPI:
    def __init__(self, config) -> None:
        self.host_url = config['host']

    def _convert_timestamp_to_date(self, timestamp):
        return timestamp.strftime(TIMEFORMAT)

    def _get_water_level_at_timestamp(self, params={}):
        
        params_dict = {}
        params_dict.update(params)

        url = self.host_url + str.format(WATER_LEVEL_API, **params_dict)
        data = requests.get(url).json()
        
        extracted_data = self._data_extraction(data)
        return extracted_data

    def _data_extraction(self, data):
        camera_id = data['CameraId']
        timestamp = data['Timestamp']
        reading1 = data['Reading']
        reading2 = data['Reading2']

        # timestamp = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
        # date = self._convert_timestamp_to_date(timestamp)
        return {
            'camera_id': camera_id, 
            'timestamp': timestamp, 
            'reading1': reading1, 
            'reading2': reading2
        }

    def _save_data_to_db(self, data):
        df = pd.read_csv(DATABASE)
        data_df = pd.DataFrame(data, columns=data.keys())
        df = df.append(data_df)
        df.to_csv(DATABASE, index=False)

    def _convert_db_to_graph(self, camera_id, type = 'hourly'):
        assert type in ['hourly', 'daily', 'monthly']

        df = pd.read_csv(DATABASE)
        df_city = df[df.camera_id==camera_id]

        self.make_graph_csv(df_city)

        graph_json = json.load(open('./static/data/chart.json', encoding='utf-8'))
        return graph_json

    def make_graph_csv(self, city_df):
        graph_json = []
        graph_info = [i for i in zip(
            city_df.camera_id,
            city_df.timestamp,
            city_df.reading1,
            city_df.reading2)]
        
        for cam_id, timestamp, reading1, reading2 in graph_info:
            graph_json.append({
                'camera_id': cam_id,
                'timestamp': timestamp,
                'type': 'reading1',
                'value': reading1
            })

            graph_json.append({
                'camera_id': cam_id,
                'timestamp': timestamp,
                'type': 'reading2',
                'value': reading2
            })

        pd.DataFrame(graph_json).to_csv('./static/data/graph.csv', index=False)

    def crawl_data(self, camera_ids, from_date, to_date=None, step=1, type='hourly'):
        assert type in ['hourly', 'daily', 'monthly']

        from_date = datetime.strptime(from_date, '%Y-%m-%d')

        if to_date is None:
            to_date = datetime.now()
        else:
            to_date = datetime.strptime(to_date, '%Y-%m-%d')

        if type == 'hourly':
            time_iter = hourly_it(from_date, to_date, step)
        if type == 'daily':
            time_iter = daily_it(from_date, to_date, step)

        result_dict = {
            'camera_id': [], 
            'timestamp': [], 
            'reading1': [], 
            'reading2': []
        }
        for time in tqdm(time_iter):
            time_format = self._convert_timestamp_to_date(time)

            for camera_id in camera_ids:
                extracted_data = self._get_water_level_at_timestamp(params={
                    'city_name': camera_id,
                    'time_stamp': time_format
                })

                for key, value in extracted_data.items():
                    result_dict[key].append(value)

        self._save_data_to_db(result_dict)

def nearest_date(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))

def hourly_it(start, finish, step=1):
    while finish > start:
        start = start + timedelta(hours=step)
        yield start

def daily_it(start, finish, step=1):
    while finish > start:
        start = start + timedelta(days=step)
        yield start
