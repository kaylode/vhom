import os
import json
import folium
import requests
import pandas as pd

from .utils import read_csv, add_markers

STATICS_DIR = './statics'
overlay_path = './data/geojson/vietnam.geojson'
csv_path = './data/csv/vn_provinces.csv'


def get_map():

    # Init map
    my_map = folium.Map(location=[16.3, 106.72], zoom_start=6)

    # Overlay provinces
    folium.GeoJson(overlay_path, name="geojson").add_to(my_map)

    # Read data and coloring
    df = read_csv(csv_path)
    folium.Choropleth(
        geo_data=overlay_path,
        name="choropleth",
        data=df,
        columns=["name", "population"],
        key_on="feature.properties.name",
        fill_color="YlGn",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Population",
    ).add_to(my_map)

    add_markers(my_map, df)


    folium.LayerControl().add_to(my_map)
    my_map.save(os.path.join(STATICS_DIR,"index.html"))

    return my_map