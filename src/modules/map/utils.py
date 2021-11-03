import os
import json
import folium
import pandas as pd


def get_info_from_json(path):
    with open(path, 'r', encoding='utf8') as f:
        states = json.load(f)

    cordinates = []
    features = states['features']

    for city_feat in features:
        name = city_feat['properties']['name']
        camera_id = city_feat['properties']['camera_id']
        long, lat = city_feat['geometry']['coordinates']
        cordinates.append([name, lat, long, camera_id])

    return cordinates

def get_icon(image_path=None, icon_color=None):
    """
    Get custom icon for markers
    """
    from folium.features import CustomIcon
    
    if image_path is not None:
        icon = CustomIcon(
            image_path,
            icon_size=(64, 64),
            icon_anchor=(32, 63),
        )
    else:
        if icon_color is not None:
            icon = folium.Icon(color=icon_color, icon='tint')
        else:
            icon = None

    return icon