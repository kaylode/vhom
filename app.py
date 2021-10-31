import os
from modules import MyMap, WaterLevelAPI, BackgroundTasks, DATABASE
from configs import Config
from flask import Flask, render_template, jsonify, request

app_config = Config('./configs/config.yaml')
map_config = app_config.map
api_config = app_config.api
API = WaterLevelAPI(api_config)

app = Flask(__name__, template_folder=map_config['template_dir'], static_url_path="/web/static", static_folder="web/static")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/')
def map():
    folium_map = MyMap(map_config)
    folium_map.save_html(os.path.join(map_config['template_dir'],"index.html"))
    return render_template("index.html")

@app.route('/data')
def data():
    plot_type = request.args.get('type', default = 'hourly', type = str)
    camera_id = request.args.get('cameraId', default = 'tvmytho', type = str)

    json_graph = DATABASE._convert_db_to_graph(
        table_name='waterlevel',
        filter_dict={
            'camera_id': camera_id
        }
    )
    return jsonify(json_graph)

@app.route('/request')
def requests():
    
    data = API.crawl_data(
        camera_ids=['tvmytho', 'tvlongdinh'],
        from_date='2021-10-27T00:00:00',
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
    DATABASE.connect()
    # thread = BackgroundTasks(API, DATABASE, run_every_sec=30)
    # thread.start()
    app.run(debug=True)
    # thread.break_loop()
