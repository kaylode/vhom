import psycopg2
from psycopg2 import sql
import json
import pandas as pd
from datetime import datetime
from configparser import ConfigParser

class PostgreSQLDatabase:
    def __init__(self, config_file, section) -> None:
        self.config = self.load_config(config_file, section)
        self.cursor = None
        self.connection = None
    
    def load_config(self, filename, section):
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
            raise Exception(
                "Section {0} not found in the {1} file".format(section, filename)
            )

        return db

    def connect(self, config_params={}):

        self.config.update(config_params)

        """ Connect to the PostgreSQL database server """
        self.connection = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            self.connection = psycopg2.connect(**self.config)
            
            # create a cursor
            self.cursor = self.connection.cursor()
            
            # execute a statement
            print('PostgreSQL database version:')
            self.cursor.execute('SELECT version()')

            # display the PostgreSQL database server version
            db_version = self.cursor.fetchone()
            print(db_version)

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.connection is not None:
            self.connection.close()
            print('Database connection closed.')

    def check_table_exist(self, table_name):
        comand = """select exists(select * from information_schema.tables where table_name=%(table_name)s)"""
        self.cursor.execute(comand, {
            'table_name': table_name
        })
        return bool(self.cursor.rowcount)

    def create_table(self, table_name, column_dict={}):

        if self.check_table_exist(table_name):
            print("Table exists")
            return

        colum_string = []
        for key, value in column_dict.items():
            colum_string.append(f"{key} {value}")
        
        colum_string = ", ".join(colum_string)

        command = f"""
        create table {table_name} (
            {colum_string}
        )
        """
        try:
            self.cursor.execute(command)
            self.connection.commit()
        except psycopg2.errors.DuplicateTable:
            print(f"Table {table_name} is aldreay existed")

    def check_row_exists(self, table_name, condition_dict):
        
        colum_string = []
        for key, value in condition_dict.items():
            colum_string.append(f"{key}='{value}'")
        
        colum_string = ' and '.join(colum_string)

        command = f"""
            select exists(select 1 from {table_name} where {colum_string})
        """

        try:
            self.cursor.execute(command)
            row = self.cursor.fetchone()[0]
        except psycopg2.errors.DuplicateTable:
            print(f"Table {table_name} is aldreay existed")
         
        return row
    
    def _crawl_data_on_daily(self, api, camera_ids, lasted_date, step=0.5):
        data = api.crawl_data(
            camera_ids=camera_ids,
            from_date = lasted_date,
            step = step
        )
        try:
            response = self._save_data_to_db(data)
        except:
            response = {
                "status": 404,
                "reponse": "Failed to save"
            }
        return response

    def _db_to_json(self, rows):
        """
        Convert dataframe to json
        :params:
            dataframe: dataframe need to be converted
        :returns:
            vega json: vega plot file. Will be rendered by Javascripts
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
        Convert database to graph
        :params:
            filter_fn: database filter function
        :returns:
            vega json: vega plot file. Will be rendered by Javascripts
        """

        if filter_dict is not None:
            filter_string = []
            for key, value in filter_dict.items():
                filter_string.append(f"{key}='{value}'")
            filter_string = ' and '.join(filter_string)

        if filter_dict is not None:
            command = f"""
                select * from {table_name} where {filter_string}
            """
        else:
            command = f"""
                select * from {table_name}
            """
        
        self.cursor.execute(command)
        rows = self.cursor.fetchall()

        # Convert database to json format, then save to visualize VEGA plot
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
        
        for values in dict_iter:
            command = sql.SQL("""insert into {}(camera_id, timestamp, reading1, reading2) values(%s, %s, %s, %s)""").format(sql.Identifier(table_name))

            self.cursor.execute(command, [*values])
        self.connection.commit()
        
        return {
            "status": 202,
            "reponse": "Successfully saved"
        }

    def _get_last_date(self, table_name, filter_dict=None):
        """
        Get lastest date, if database is empty, get now
        """
        if filter_dict is not None:
            filter_string = []
            for key, value in filter_dict.items():
                filter_string.append(f"{key}='{value}'")
            filter_string = ' and '.join(filter_string)
            command = f"select max(timestamp) from {table_name} where {filter_string}"
        else:
            command = sql.SQL("""select max(timestamp) from {}""").format(sql.Identifier(table_name))
        
        self.cursor.execute(command)
        timestamp = self.cursor.fetchone()[0]
        return timestamp

    def __del__(self):
        """
        Destructor
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