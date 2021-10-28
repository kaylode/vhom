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

@app.route('/map')
def map():
    folium_map = MyMap(map_config)
    folium_map.save_html(os.path.join(map_config.template_dir,"index.html"))
    return render_template("index.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def request():
    api = MyAPI(api_config)
    return data

# @app.route('/data')
# def data():
#     plot_type = request.args.get('type', default = 'bar', type = str)
#     j = json.load(open('./static/data/bar.json'))
#     j['mark'] = plot_type
#     return jsonify(j)

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
    app.run(debug=True)
    