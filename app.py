import os
import json
import folium
import requests
import pandas as pd


STATICS_DIR = './statics'
overlay_path = './data/geojson/vietnam.geojson'
csv_path = './data/csv/vn_provinces.csv'

def read_csv(path):
    df = pd.read_csv(path)
    small_df = df[['admin_name', 'lat', 'lng',  'population']]
    small_df.columns = ['name', 'lat', 'lng',  'population']
    small_df = small_df.dropna()
    small_df = small_df.drop_duplicates(['name'])
    return small_df


""" Custom icon
from folium.features import CustomIcon


m = folium.Map(location=[45.372, -121.6972], zoom_start=12, tiles="Stamen Terrain")

url = "http://leafletjs.com/examples/custom-icons/{}".format
icon_image = url("leaf-red.png")
shadow_image = url("leaf-shadow.png")

icon = CustomIcon(
    icon_image,
    icon_size=(38, 95),
    icon_anchor=(22, 94),
    shadow_image=shadow_image,
    shadow_size=(50, 64),
    shadow_anchor=(4, 62),
    popup_anchor=(-3, -76),
)

"""

# from folium.features import GeoJsonPopup, GeoJsonTooltip
# tooltip = GeoJsonTooltip(
#     fields=["name", "medianincome", "change"],
#     aliases=["State:", "2015 Median Income(USD):", "Median % Change:"],
#     localize=True,
#     sticky=False,
#     labels=True,
#     style="""
#         background-color: #F0EFEF;
#         border: 2px solid black;
#         border-radius: 3px;
#         box-shadow: 3px;
#     """,
#     max_width=800,
# )


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

if __name__ == '__main__':

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