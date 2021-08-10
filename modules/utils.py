import os
import json
import folium
import vincent
import requests
import numpy as np
import pandas as pd

def process_df(path):
    df = pd.read_csv(path)
    small_df = df[['admin_name', 'lat', 'lng',  'population']]
    small_df.columns = ['name', 'lat', 'lng',  'population']
    small_df = small_df.dropna()
    small_df = small_df.drop_duplicates(['name'])
    cordinates = [i for i in zip(small_df.name, small_df.lat, small_df.lng)]

    return cordinates

def get_icon(image_path=None, shadow_path=None, icon_color=None):
    """
    Get custom icon for markers
    """
    from folium.features import CustomIcon
    
    if image_path is not None:
        icon = CustomIcon(
            image_path,
            icon_size=(38, 95),
            icon_anchor=(22, 94),
            shadow_image=shadow_path,
            shadow_size=(50, 64),
            shadow_anchor=(4, 62),
            popup_anchor=(-3, -76),
        )
    else:
        if icon_color is not None:
            icon = folium.Icon(color=icon_color)
        else:
            icon = None

    return icon

def request_data(url):
    """
    Send request data and convert format
    """
    data = requests.get(url).json() # dict(name: dict(date:value))
    
    for location in data.keys():
        date_row = list(data[location].keys())
        value_col = list(data[location].value())

    df = pd.DataFrame(list(zip(date_row, value_col)),
               columns =['Date', 'Value'])

    # Vincent chart
    line_chart = vincent.Line(df, width=600, height=300)
    line_chart.axis_titles(x='Date', y='Value')
    line_chart.legend(title='Water Level by Date')

    # Convert it to JSON.
    scatter_json = line_chart.to_json()
    return scatter_json

def get_vega_popup(json):
    # Let's create a Vega popup based on scatter_json.
    popup = folium.Popup(max_width=450)
    popup.add_child(folium.Vega(json, width=450, height=250))
    return popup