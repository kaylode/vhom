import psycopg2
from psycopg2 import sql
import pandas as pd
from datetime import datetime, timedelta
from configparser import ConfigParser
from modules.logger import LoggerManager

LOGGER = LoggerManager.init_logger(__name__)

class PostgreSQLDatabase:
    """
    PostgreSQL database Python interation
    """
    def __init__(self, config_file, section) -> None:
        self.config = self.load_config(config_file, section)
        self.cursor = None
        self.connection = None
    
    def load_config(self, filename, section):
        """
        Load database config from .ini file
        :params:
            filename:   path to .ini file
            section:    section in .ini file to be loaded
        :returns:
            dict contains database config
        """
        parser = ConfigParser()
        # read config file
        parser.read(filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(section):
            params = parser.items(section)
            for param in params:
                db[param[0]] = param[1]
        else:
            LOGGER.error("Section {0} not found in the {1} file".format(section, filename))
            raise Exception()

        return db

    def connect(self, config_params={}):
        """
        Start connection to database
        """
        self.config.update(config_params)

        """ Connect to the PostgreSQL database server """
        self.connection = None
        try:
            # connect to the PostgreSQL server
            LOGGER.info('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**self.config)
            
            # create a cursor
            self.cursor = self.connection.cursor()
            
            # execute a statement
            self.cursor.execute('SELECT version()')
            db_version = self.cursor.fetchone()

            # Logging
            LOGGER.info(f'PostgreSQL database version: {db_version}')

        except (Exception, psycopg2.DatabaseError) as error:
            LOGGER.error(error)

    def close(self):
        """
        Close the connection to database
        """
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
            LOGGER.info('Database connection closed.')
                    
    def create_table(self, table_name, column_dict={}):
        """
        Create table in the database
        :params:
            table_name: name of the table
            column_dict: dict of column's names and its type. Example:
                {
                    'id': 'integer primary key'
                }
        """

        # Convert column dict to string
        colum_string = []
        for key, value in column_dict.items():
            colum_string.append(f"{key} {value}")
        colum_string = ", ".join(colum_string)

        # Make the command
        command = f"""
        create table {table_name} (
            {colum_string}
        )
        """

        # Execute command
        try:
            self.cursor.execute(command)
            self.connection.commit()
        except psycopg2.errors.DuplicateTable:
            LOGGER.info(f"Table {table_name} is already existed")
            self.connection.rollback()

    def check_row_exists(self, table_name, condition_dict):
        """
        Check whether a duplicate row exists
        :params:
            table_name: name of the table
            condition_dict: dict of condition to be checked
        """

        # Convert column dict to string
        colum_string = []
        for key, value in condition_dict.items():
            colum_string.append(f"{key}='{value}'")
        colum_string = ' and '.join(colum_string)

        # Make command
        command = f"""
            select exists(select 1 from {table_name} where {colum_string})
        """

        try:
            # Execute command
            self.cursor.execute(command)
            row = self.cursor.fetchone()[0]
        except Exception as e:
            LOGGER.error(e)
            return None
 
        return row
    
    def _crawl_data_on_daily(self, table_name, api, camera_ids, lasted_date, step=0.5):
        """
        Crawl data from API server then save to database
        """
        data = api.crawl_data(
            camera_ids=camera_ids,
            from_date = lasted_date,
            step = step
        )
        response = self._save_data_to_db(data, table_name)
        return response

    def _db_to_json(self, rows):
        """
        Convert database to json
        :params:
            rows: records which are fetched all from database
        :returns:
            list of dict
        """
    
        graph_json = []

        for _, cam_id, timestamp, reading1, reading2 in rows:
            timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%S')
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

    def _convert_db_to_graph(self, graph_csv, table_name, filter_dict=None):
        """
        Convert database to graph, save to csv file
        :params:
            graph_csv: output csv
            table_name: name of the table
            filter_dict: database filter dict
        """

        # Make condition string
        if filter_dict is not None:
            filter_string = []
            for key, value in filter_dict.items():
                filter_string.append(f"{key}='{value}'")
            filter_string = ' and '.join(filter_string)

        # Filter out uncessary records
        if filter_dict is not None:
            command = f"""
                select * from {table_name} where {filter_string}
            """
        else:
            command = f"""
                select * from {table_name}
            """
        
        try:
            # Execute command
            self.cursor.execute(command)
            rows = self.cursor.fetchall()
        except Exception as e:
            LOGGER.error(e)
            rows = []

        # Convert database to json format, then save as csv to visualize VEGA plot
        graph_json = self._db_to_json(rows)
        pd.DataFrame(graph_json).to_csv(graph_csv, index=False)
        
    def _save_data_to_db(self, data, table_name):
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

        if self.connection is None:
            self.connect()

        dict_iter = zip(*data.values())

        try:
            for values in dict_iter:

                # Check if row is already existed
                if self.check_row_exists(table_name, condition_dict={
                        'camera_id': values[0],
                        'timestamp': values[1],
                    }):
                    continue
                
                # Make command
                command = sql.SQL("""insert into {}(camera_id, timestamp, reading1, reading2) values(%s, %s, %s, %s)""").format(sql.Identifier(table_name))

                # Execute command
                self.cursor.execute(command, [*values])

            # Confirm updating database
            self.connection.commit()
        except Exception as e:
            LOGGER.error(e)
            self.connection.rollback()

            return {
                "status": 404,
                "reponse": "Database failed to update"
            }
        
        return {
            "status": 202,
            "reponse": "Database saved successfully"
        }

    def _get_last_date(self, table_name, filter_dict=None):
        """
        Get lastest date from database
        :returns:
            lastest timestamp
        """
        if filter_dict is not None:
            filter_string = []
            for key, value in filter_dict.items():
                filter_string.append(f"{key}='{value}'")
            filter_string = ' and '.join(filter_string)
            command = f"select max(timestamp) from {table_name} where {filter_string}"
        else:
            command = sql.SQL("""select max(timestamp) from {}""").format(sql.Identifier(table_name))
        
        try:
            self.cursor.execute(command)
            timestamp = self.cursor.fetchone()[0]
        except Exception as e:
            LOGGER.error(e)
            timestamp = self._get_yesterdate()

        if timestamp is None:
            timestamp = self._get_yesterdate()
        
        return str(timestamp)

    def _get_aggregated_value(self, table_name, column, camera_id, from_date=None, to_date=None, aggr='avg'):
        """
        Get average value from column
        """
        assert aggr in ['avg', 'max', 'min']

        if from_date is None:
            from_date = self._get_yesterdate()

        if to_date is None:
            to_date = datetime.now()
            to_date = to_date.strftime('%Y-%m-%d %H:%M:%S')

        command = f"select {aggr}({column}) from {table_name} where timestamp between '{from_date}' and '{to_date}' and camera_id = '{camera_id}'"
    
        try:
            self.cursor.execute(command)
            value = self.cursor.fetchone()[0]
            if value is None:
                raise ValueError("No columns found")
        except Exception as e:
            LOGGER.error(e)
            value = 0
            
        return value    

    def _get_yesterdate(self):
        """
        Get system the day before today.
        """
        now = datetime.now()
        delta = timedelta(days = 1)
        yesterday = now - delta
        return yesterday.strftime('%Y-%m-%d %H:%M:%S')
        

    def __del__(self):
        """
        Destructor. Close database connection when object is destroyed
        """
        self.close()


if __name__ == '__main__':
    db = PostgreSQLDatabase()
    db.connect()

    db.create_table(
        table_name='waterlevel',
        column_dict = {
            'id': "serial primary key",
            'camera_id': "varchar(30) not null",
            'timestamp': "timestamp",               #'2016-06-22 19:10:25-07'
            'reading1': "double precision",
            'reading2': "double precision",
        }
    )