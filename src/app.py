import json
import os
from modules import MyMap, MyAPI
from configs import Config
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app_config = Config('./configs/config.yaml')
map_config = app_config.map
api_config = app_config.api
server_config = app_config.server

api = MyAPI(api_config)

@app.route('/')
def map():
    folium_map = MyMap(map_config)
    folium_map.save_html(os.path.join(map_config['template_dir'],"index.html"))
    return render_template("index.html")

@app.route('/data')
def data():
    plot_type = request.args.get('type', default = 'hourly', type = str)
    camera_id = request.args.get('cameraId', default = 'tvmytho', type = str)
    json_graph = api._convert_db_to_graph(camera_id, type=plot_type)
    return jsonify(json_graph)

@app.route('/request')
def requests():
    
    api.crawl_data(
        camera_ids=['tvlongdinh', 'tvmytho'],
        from_date='2021-09-03',
    )
    return jsonify({
        '202': 'Successfully crawled'
    })

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
    app.run(
        host=server_config['host'], port=server_config['port'], threaded=True
    )    