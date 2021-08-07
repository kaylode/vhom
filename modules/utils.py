import os
import json
import folium
import requests
import pandas as pd

def read_csv(path):
    df = pd.read_csv(path)
    small_df = df[['admin_name', 'lat', 'lng',  'population']]
    small_df.columns = ['name', 'lat', 'lng',  'population']
    small_df = small_df.dropna()
    small_df = small_df.drop_duplicates(['name'])
    return small_df


def add_markers(map, df):
    cordinates = [i for i in zip(df.name, df.lat, df.lng)]

    for name, lat, long in cordinates:

        # html = """
        #     <h1> This popup is an Iframe</h1><br>
        #     With a few lines of code...
        #     <p>
        #     <code>
        #         from numpy import *<br>
        #         exp(-2*pi)
        #     </code>
        #     </p>
        #     """

        # iframe = branca.element.IFrame(html=html, width=500, height=300)
        # popup = folium.Popup(iframe, max_width=500)

        # folium.Marker([30, -100], popup=popup).add_to(m)

        folium.Marker(
            location=[lat, long],
            popup=name
        ).add_to(map)