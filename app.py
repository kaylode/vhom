from flask import Flask, render_template
import folium
from modules import get_map, request_data

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/map')
def map():
    folium_map = get_map()
    # return folium_map._repr_html_()
    return render_template("index.html")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/data')
def request():
    data = request_data('http://192.168.100.16:4000/api/request')
    return data

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