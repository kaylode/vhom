import os

import json
from modules import MyMap, WaterLevelAPI, BackgroundTasks, PostgreSQLDatabase
from configs import Config, ConfigDict
from flask import Flask, render_template, jsonify, request

###   CONFIGURATION     ####
# app_config = Config('configs/config.yaml')
app_config = ConfigDict('configs/config.json')
map_config = app_config.map
api_config = app_config.api
db_config = app_config.database
server_config = app_config.server

###     INITIALIZE FLASK        ###
app = Flask(__name__, 
    template_folder=map_config['template_dir'], 
    static_url_path='/'+map_config['static_dir'], 
    static_folder=map_config['static_dir'])
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


###     ROUTING        ####
@app.route('/')
def map():
    folium_map = MyMap(map_config)

    if not os.path.exists(map_config['template_dir']):
        os.mkdir(map_config['template_dir'])

    folium_map.save_html(os.path.join(map_config['template_dir'],"index.html"))
    return render_template("index.html")

@app.route('/info')
def info():
    return render_template("info.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")

@app.route('/data')
def data():
    camera_id = request.args.get('cameraId', default = 'tvmytho', type = str)

    DATABASE._convert_db_to_graph(
        graph_csv='./web/static/data/graph.csv',
        table_name='waterlevel',
        filter_dict={
            'camera_id': camera_id
        }
    )

    json_graph = json.load(open(map_config['vega_chart'], encoding='utf-8'))
    return jsonify(json_graph)


@app.route('/stat')
def stat():
    camera_id = request.args.get('cameraId', default = 'tvmytho', type = str)

    result_dict = {}
    for reading in ['reading1', 'reading2']:
        reading_dict = {}
        for aggr in ['min', 'max', 'avg']:
            value = DATABASE._get_aggregated_value(
                table_name='waterlevel',
                camera_id = camera_id,
                column=reading,
                aggr=aggr
            )

            reading_dict[aggr] = round(float(value))
        result_dict[reading] = reading_dict

    return jsonify(result_dict)

@app.route('/request')
def requests():
    
    data = API.crawl_data(
        camera_ids=['tvmytho', 'tvlongdinh'],
        from_date='2021-10-27 00:00:00',
    )

    try:
        response = DATABASE._save_data_to_db(data, table_name='waterlevel')
    except:
        response = {
            "status": 404,
            "reponse": "Failed to save"
        }

    return jsonify(response)

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

if __name__ == '__main__':

    print(app_config)

    ## Initiate API
    API = WaterLevelAPI(api_config)

    ## Initiate database
    DATABASE = PostgreSQLDatabase(
        config_file = db_config['filename'],
        section = db_config['section'])

    DATABASE.connect()

    DATABASE.create_table(
        table_name='waterlevel',
        column_dict = {
            'id': "serial primary key",
            'camera_id': "varchar(30) not null",
            'timestamp': "timestamp",               # %Y-%m-%d %H:%M:%S'
            'reading1': "double precision",
            'reading2': "double precision",
        }
    )

    ## Start Flask App

    thread = BackgroundTasks(API, DATABASE, run_every_sec=30*60)
    thread.start()

    app.run(
        host=server_config['host'], port=server_config['port'], use_reloader=False, debug=True
    )    
    thread.break_loop()
