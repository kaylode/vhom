import folium
from .utils import process_df, get_icon
from .custom import OnClickMarker
from branca.element import CssLink, JavascriptLink, Element

class MyMap:
    """
    My custom map class
    """
    def __init__(self, config):

        self.init_location = config['location']
        self.init_zoom = config['zoom']

        # Init map
        self.map = folium.Map(
            location=self.init_location, 
            zoom_start=self.init_zoom)

        self.add_overlay(config['overlay'])
        self.add_markers(
            cordinates=process_df(config['cordinates']),
            icon=config['icon_path'])

        self.init_headers()
        self.init_body()
    
    def add_overlay(self, overlay_path):
        """
        Add overlay to map
        """
        overlay = folium.GeoJson(overlay_path, name="geojson")
        overlay.add_to(self.map)

    def add_markers(self, cordinates, icon=None):
        """
        Add pre-defined markers to map
        """

        for name, lat, long, camera_id in cordinates:

            # Data with each marker, when clicked, client receive 
            marker_data = {
                'Camera id': camera_id,
                'Trạm thủy văn': name,
                'Kinh độ': str(long),
                'Vĩ độ': str(lat),
            }

            marker = OnClickMarker(
                location=[lat, long],
                popup=name,
                icon=get_icon(icon, icon_color='blue'),
                on_click="onMarkerClick",
                on_click_data=marker_data)

            marker.add_to(self.map)

    def save_html(self, path):
        """
        Save map to static html file
        """
        folium.LayerControl().add_to(self.map)
        self.map.save(path)

    def init_headers(self):
        """
        Add JavaScript libraries, CSS files
        """
        from .custom import CustomJavaScript
        self.map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/style.css') }}"))
        self.map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/tailwind.css') }}"))
        self.map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/w3.css') }}"))
        self.map.get_root().html.add_child(JavascriptLink("{{ url_for('static', filename='js/main.js') }}"))
        self.map.get_root().header.add_child(JavascriptLink("{{ url_for('static', filename='js/jquery-3.5.1.min.js') }}"))
        self.map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega@5"))
        self.map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@5"))
        self.map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@6"))

    def init_body(self):
        """
        Add custom body HTML
        """
        
        html_body = '''
        <div class="w3-bar w3-blue">
            <a href="#" class="w3-bar-item w3-mobile w3-yellow w3-middle w3-large">Vietnam Water level map</a>
            <a href="#" class="w3-bar-item w3-button w3-hover-green w3-right"><i class="fa fa-search"></i></a>
            <input type="text" class="w3-bar-item w3-input w3-right" placeholder="Search..">
            <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large w3-right"><i class="fa fa-envelope"></i></a>
            <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large w3-right"><i class="fa fa-home"></i></a>
        </div>        

        <div class="div_float" id="float_panel">
            <span id='close'>x</span><br>
            <div class="w3-dropdown-hover">
            <button id="dropdown" class="w3-button w3-green">▼ Biểu đồ theo giờ</button>
                <div class="w3-dropdown-content w3-bar-block w3-card-4">
                    <a href="#" id="type1" class="w3-bar-item w3-button">Biểu đồ theo giờ</a>
                    <a href="#" id="type2" class="w3-bar-item w3-button">Biểu đồ theo ngày</a>
                </div>
            </div>
            <br>
            <div id="vis"></div>
            
        </div>

        <div class="div_float" id="float_panel2">
        <p id="city-info"></p>
        </div>

        '''
        self.map.get_root().html.add_child(Element(html_body))

    