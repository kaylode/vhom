import os
import json
import folium
import vincent
import requests
import numpy as np
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

        # popup = get_vega_popup(json.load(open('./static/data/bar2.json','r')))
        OnClickMarker(
            location=[lat, long],
            popup=name,
            on_click="onClick"
        ).add_to(map)

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

def get_icon():
    """
    Get custom icon for markers
    """
    from .constant import ICON_PATH
    from folium.features import CustomIcon

    if ICON_PATH is None:
        return None

    icon_image = ICON_PATH

    icon = CustomIcon(
        icon_image,
        icon_size=(38, 95),
        icon_anchor=(22, 94),
        # shadow_image=shadow_image,
        shadow_size=(50, 64),
        shadow_anchor=(4, 62),
        popup_anchor=(-3, -76),
    )

    return icon

def get_map(location=[16.3, 106.72], zoom_start=6):
    """
    Get map, init with location and zoom
    """
    from .constant import OVERLAY_PATH, CORDINATE_PATH, TEMPLATE_DIR

    # Init map
    my_map = folium.Map(location=location, zoom_start=zoom_start)
    
    # add provinces overlay
    folium.GeoJson(OVERLAY_PATH, name="geojson").add_to(my_map)

    # Add markers
    df = read_csv(CORDINATE_PATH)
    add_markers(my_map, df)

    add_custom_files(my_map)
    folium.LayerControl().add_to(my_map)
    my_map.save(os.path.join(TEMPLATE_DIR,"index.html"))

    return my_map

def add_custom_files(map):
    from branca.element import CssLink, JavascriptLink, Element
    
    map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/style.css') }}"))
    map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/w3.css') }}"))
    map.get_root().html.add_child(JavascriptLink("{{ url_for('static', filename='js/functions.js') }}"))
    map.get_root().header.add_child(JavascriptLink("{{ url_for('static', filename='js/jquery-3.5.1.min.js') }}"))
    map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega@5"))
    map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@5"))
    map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@6"))

    html_body = '''
    <div class="w3-bar w3-blue">
        <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large w3-right">Home</a>
        <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large w3-right">About</a>
        <input type="text" class="w3-bar-item w3-input w3-right" placeholder="Search..">
        <a href="#" class="w3-bar-item w3-button w3-green w3-right">Go</a>
    </div>        

    <div class="div_float" id="float_panel">
        <span id='close'>x</span>
        <div id="vis"></div>
    </div>

    '''
    map.get_root().html.add_child(Element(html_body))