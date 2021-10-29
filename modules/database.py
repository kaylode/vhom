import json
import pandas as pd
from datetime import datetime
import asyncio

DATABASE_CSV = './data/database/db.csv'
GRAPH_CSV = './static/data/graph.csv'
CHART_JSON = './static/data/chart.json'

class Database:
    def __init__(self) -> None:
        self.path = DATABASE_CSV

    def background_crawl(self, **kwargs):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(self._crawl_data_on_daily(**kwargs))
        return response

    async def _crawl_data_on_daily(self, api, camera_id, lasted_date):
        data = api.crawl_data(
            camera_ids=[camera_id],
            from_date = lasted_date,
        )
        try:
            response = self._save_data_to_db(data)
        except:
            response = {
                "status": 404,
                "reponse": "Failed to save"
            }
        return response
        
    def _save_data_to_db(self, data):
        """
        Save data to database
        :params:
            data: dict for dataframe update. 
                Example:   result_dict = {
                    'camera_id': [], 
                    'timestamp': [], 
                    'reading1': [], 
                    'reading2': []
                }
        """

        df = pd.read_csv(self.path)
        data_df = pd.DataFrame(data, columns=data.keys())
        df = df.append(data_df)
        df.to_csv(self.path, index=False)
        return {
            "status": 202,
            "reponse": "Successfully saved"
        }

    def _get_db(self):
        """
        Get database
        """
        df = pd.read_csv(self.path)
        return df

    def _get_last_date(self, filter_fn=None):
        """
        Get lastest date, if database is empty, get now
        """

        df = pd.read_csv(self.path)
        if filter_fn is not None:
            df = filter_fn(df)

        if len(df) == 0:
            timestamp = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
        else:
            timestamp = df.iloc[-1].timestamp

        return timestamp

    def _convert_db_to_graph(self, filter_fn=None):
        """
        Convert database to graph
        :params:
            filter_fn: database filter function
        :returns:
            vega json: vega plot file. Will be rendered by Javascripts
        """

        df = pd.read_csv(self.path)

        if filter_fn is not None:
            df = filter_fn(df)

        # Convert database to json format, then save to visualize VEGA plot
        graph_json = self._df_to_json(df)
        pd.DataFrame(graph_json).to_csv(GRAPH_CSV, index=False)

        # Return vega json
        return json.load(open(CHART_JSON, encoding='utf-8'))

    def _df_to_json(self, dataframe):
        """
        Convert dataframe to json
        :params:
            dataframe: dataframe need to be converted
        :returns:
            vega json: vega plot file. Will be rendered by Javascripts
        """
        graph_json = []
        graph_info = [i for i in zip(
            dataframe.camera_id,
            dataframe.timestamp,
            dataframe.reading1,
            dataframe.reading2)]
        
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
        
        return graph_json


## Initiate database
DATABASE = Database()