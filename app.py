from flask import Flask
import folium
from modules import get_map, request_data

app = Flask(__name__)


@app.route('/map')
def index():
    folium_map = get_map()
    return folium_map._repr_html_()

@app.route('/data')
def request():
    data = request_data('http://192.168.100.16:4000/api/request')
    return data

if __name__ == '__main__':
    app.run(debug=True)