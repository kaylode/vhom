import requests
from datetime import datetime
from tqdm import tqdm

from .utils import hourly_it, daily_it

class WaterLevelAPI:
    def __init__(self, config) -> None:
        self.request_template = '{city_name}/history?time={time_stamp}'
        self.date_format = "%Y-%m-%d-%H-%M-%S"
        self.host_url = config['host']

    def _convert_timestamp_to_date(self, timestamp):
        return timestamp.strftime(self.date_format)

    def _get_water_level_at_timestamp(self, params={}):
        
        params_dict = {}
        params_dict.update(params)

        url = self.host_url + str.format(self.request_template, **params_dict)
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

    def crawl_data(self, camera_ids, from_date, to_date=None, step=1, type='hourly'):
        assert type in ['hourly', 'daily', 'monthly']

        from_date = datetime.strptime(from_date, '%Y-%m-%dT%H:%M:%S')

        if to_date is None:
            to_date = datetime.now()
        else:
            to_date = datetime.strptime(to_date, '%Y-%m-%dT%H:%M:%S')

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
        for camera_id in camera_ids:
            for time in tqdm(time_iter):
                time_format = self._convert_timestamp_to_date(time)

                extracted_data = self._get_water_level_at_timestamp(params={
                    'city_name': camera_id,
                    'time_stamp': time_format
                })

                # Check if requested timestamp is unchanged
                if len(result_dict['timestamp']) > 0:
                    if extracted_data['timestamp'] == result_dict['timestamp'][-1] and extracted_data['camera_id'] == result_dict['camera_id'][-1]:
                        break

                for key, value in extracted_data.items():
                    result_dict[key].append(value)

        return result_dict