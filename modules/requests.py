import os
import json
import folium
import vincent
import requests
import numpy as np
import pandas as pd

from .utils import read_csv, add_markers

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
        
    # Let's create a Vega popup based on scatter_json.
    popup = folium.Popup(max_width=0)
    folium.Vega(scatter_json, height=350, width=650).add_to(popup)
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


    folium.LayerControl().add_to(my_map)

    add_custom_files(my_map)
    my_map.save(os.path.join(TEMPLATE_DIR,"index.html"))

    return my_map

def add_custom_files(map):
    from branca.element import CssLink, JavascriptLink, Element
    
    map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/style.css') }}"))
    map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/w3.css') }}"))
    map.get_root().html.add_child(JavascriptLink("{{ url_for('static', filename='js/w3.js') }}"))
    map.get_root().header.add_child(JavascriptLink("{{ url_for('static', filename='js/jquery-3.5.1.min.js') }}"))

    html_body = '''
    <div class="w3-bar w3-blue">
        <a href="#" class="w3-bar-item w3-button w3-mobile w3-large">Home</a>
        <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large">About</a>
        <input type="text" class="w3-bar-item w3-input" placeholder="Search..">
        <a href="#" class="w3-bar-item w3-button w3-green">Go</a>
    </div>        
    '''
    map.get_root().html.add_child(Element(html_body))