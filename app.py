from flask import Flask
import folium
from modules import get_map

app = Flask(__name__)


@app.route('/map')
def index():
    folium_map = get_map()
    return folium_map._repr_html_()


if __name__ == '__main__':
    app.run(debug=True)