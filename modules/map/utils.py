import os
import json
import folium
import pandas as pd

def process_df(path):
    df = pd.read_csv(path)
    small_df = df[['city', 'lat', 'lng',  'population', 'camera_id']]
    small_df.columns = ['name', 'lat', 'lng',  'population', 'camera_id']
    small_df = small_df.dropna()
    small_df = small_df.drop_duplicates(['name'])
    cordinates = [i for i in zip(small_df.name, small_df.lat, small_df.lng, small_df.camera_id)]

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