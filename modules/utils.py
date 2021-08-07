import os
import json
import folium
import requests
import pandas as pd
from .custom import OnClickMarker

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

        OnClickMarker(
            location=[lat, long],
            popup=name,
            on_click="onClick"
        ).add_to(map)