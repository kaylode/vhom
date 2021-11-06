import requests
from datetime import datetime
from tqdm import tqdm
from .utils import hourly_it, daily_it

from modules.logger import LoggerManager
LOGGER = LoggerManager.init_logger(__name__)

class WaterLevelAPI:
    """
    Water level API, see README for more use instruction
    """
    def __init__(self, config) -> None:
        self.request_template = '{city_name}/history?time={time_stamp}'     # API request template
        self.date_format = "%Y-%m-%d-%H-%M-%S"                              # date format for API request
        self.host_url = config['host']                                      # API host server

    def _convert_timestamp_to_date(self, timestamp):
        """
        Convert datetime time to defined format
        :params:
            timestamp: datetime.datetime
        :returns:
            str: string of date
        """
        return timestamp.strftime(self.date_format)

    def _get_water_level_at_timestamp(self, params={}):
        """
        Send API request to get water level at specific timestamp
        :params:
            params: dict of parameters to input to API request template
        :returns:
            extracted_data: dict of data in right format for saving to database
        """

        # Format parameters to request template
        url = self.host_url + str.format(self.request_template, **params)

        try:
            # Send GET request to fetch data
            data = requests.get(url).json()
        except Exception as e:
            LOGGER.error(e)
            raise Exception()
        
        # Process response and return data in right format
        extracted_data = self._data_extraction(data)
        return extracted_data

    def _data_extraction(self, data):
        """
        Process response from API server
        :params:
            data: response from API request
        :returns:
            data in approriate format
        """
        camera_id = data['CameraId']
        timestamp = data['Timestamp']
        reading1 = data['Reading']
        reading2 = data['Reading2']

        return {
            'camera_id': camera_id, 
            'timestamp': timestamp, 
            'reading1': reading1, 
            'reading2': reading2
        }

    def crawl_data(self, camera_ids, from_date, to_date=None, step=1, type='hourly'):
        """
        Request data from server between specific range of time
        :params:
            camera_ids: list of camera id that need to be crawl
            from_date:  starting date
            to_date:    ending date
            step:       step between date. Measurement depends on type
            type:       to define the measurement for step
        :returns:
            result_dict = {
                'camera_id': [], 
                'timestamp': [], 
                'reading1': [], 
                'reading2': []
            }
        """
        assert type in ['hourly', 'daily', 'monthly']

        # Starting date
        from_date = datetime.strptime(from_date, '%Y-%m-%d %H:%M:%S')

        # Ending date, if to_date is None, get current date
        if to_date is None:
            to_date = datetime.now()
        else:
            to_date = datetime.strptime(to_date, '%Y-%m-%d %H:%M:%S')

        result_dict = {
            'camera_id': [], 
            'timestamp': [], 
            'reading1': [], 
            'reading2': []
        }

        # For each camera, do request
        for camera_id in camera_ids:

            # Initialize datetime iterations
            if type == 'hourly':
                time_iter = hourly_it(from_date, to_date, step)
            if type == 'daily':
                time_iter = daily_it(from_date, to_date, step)
            
            for time in tqdm(time_iter):

                # Convert timestamp to right format for API request
                time_format = self._convert_timestamp_to_date(time)

                # GET the data
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