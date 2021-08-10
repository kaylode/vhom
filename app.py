import json
import os
from modules import MyMap
from configs import Config
from modules.utils import request_data
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
map_config = Config('./configs/config.yaml')

@app.route('/map')
def map():
    folium_map = MyMap(map_config)
    folium_map.save_html(os.path.join(map_config.template_dir,"index.html"))
    return render_template("index.html")

@app.route('/')
def index():
    return render_template("index.html")

# @app.route('/data')
# def request():
#     data = request_data('http://192.168.100.16:4000/api/request')
#     return data

@app.route('/data')
def data():
    plot_type = request.args.get('type', default = 'bar', type = str)
    j = json.load(open('./static/data/bar.json'))
    j['mark'] = plot_type
    return jsonify(j)

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
    