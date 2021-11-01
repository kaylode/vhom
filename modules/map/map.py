import folium
from .utils import get_icon, get_info_from_json
from .custom import OnClickMarker
from branca.element import CssLink, JavascriptLink, Element
from folium import plugins

class MyMap:
    """
    My custom map class. Purposes:
        - Render map, icons, overlay, markers
        - Embed HTML header, body for JS scripts to work
        - Save to HTML file
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
            cordinates=get_info_from_json(config['cordinates']),
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
        
        # Use marker cluster to work with search bar
        mcg = plugins.MarkerCluster(control=False)
        self.map.add_child(mcg)

        for name, lat, long, camera_id in cordinates:

            # Data with each marker, when clicked, client receive 
            marker_data = {
                'Camera id': camera_id,
                'Trạm thủy văn': name,
                'Kinh độ': str(long),
                'Vĩ độ': str(lat),
            }

            marker = OnClickMarker(
                name=name,
                location=[lat, long],
                popup=name,
                icon=get_icon(icon, icon_color='blue'),
                on_click="onMarkerClick",
                on_click_data=marker_data)

            marker.add_to(mcg)

        self.add_search_bar(mcg)

    def add_search_bar(self, mcg):
        """
        Add search bar, search for specific location
        """
        statesearch = plugins.Search(
            layer=mcg,
            geom_type='Point',
            placeholder="Tìm kiếm trạm",
            collapsed=False,
            search_label='name',
            search_zoom=14,
            position='topleft'
        )
        
        statesearch.add_to(self.map)

    
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
        self.map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/w3.css') }}"))
        self.map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/tailwind.css') }}"))
        self.map.get_root().header.add_child(CssLink("{{ url_for('static', filename='css/style.css') }}"))
        self.map.get_root().html.add_child(JavascriptLink("{{ url_for('static', filename='js/main.js') }}"))
        self.map.get_root().header.add_child(JavascriptLink("{{ url_for('static', filename='js/jquery-3.5.1.min.js') }}"))
        self.map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega@5"))
        self.map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega-lite@5"))
        self.map.get_root().header.add_child(JavascriptLink("https://cdn.jsdelivr.net/npm/vega-embed@6"))

    def init_body(self):
        """
        Add custom body HTML
        """
        
        # html_body = '''
        # <div class="w3-bar w3-blue">
        #     <a href="#" class="w3-bar-item w3-mobile w3-yellow w3-middle w3-large">Vietnam Water level map</a>
        #     <a href="#" class="w3-bar-item w3-button w3-hover-green w3-right"><i class="fa fa-search"></i></a>
        #     <input type="text" class="w3-bar-item w3-input w3-right" placeholder="Search..">
        #     <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large w3-right"><i class="fa fa-envelope"></i></a>
        #     <a href="#" class="w3-bar-item w3-button w3-mobile w3-hover-green w3-large w3-right"><i class="fa fa-home"></i></a>
        # </div>        

        html_body = '''
        <!-- This example requires Tailwind CSS v2.0+ -->
        <div id="float_panel" class="fixed inset-0 overflow-hidden div_float w-0" aria-labelledby="slide-over-title" role="dialog" aria-modal="true">
        <div class="absolute inset-0 overflow-hidden">
            <!--
            Background overlay, show/hide based on slide-over state.

            Entering: "ease-in-out duration-500"
                From: "opacity-0"
                To: "opacity-100"
            Leaving: "ease-in-out duration-500"
                From: "opacity-100"
                To: "opacity-0"
            -->
            <div class="absolute inset-0 bg-gray-500 bg-opacity-75 transition-opacity" aria-hidden="true"></div>
            <div id="sliding_anim" class="fixed inset-y-0 right-0 pl-10 max-w-full flex transform transition ease-in-out duration-500 sm:duration-700 translate-x-full">
            <!--
                Slide-over panel, show/hide based on slide-over state.

                Entering: "transform transition ease-in-out duration-500 sm:duration-700"
                From: "translate-x-full"
                To: "translate-x-0"
                Leaving: "transform transition ease-in-out duration-500 sm:duration-700"
                From: "translate-x-0"
                To: "translate-x-full"
            -->
            <div class="relative w-screen max-w-3xl" >
                <!--
                Close button, show/hide based on slide-over state.

                Entering: "ease-in-out duration-500"
                    From: "opacity-0"
                    To: "opacity-100"
                Leaving: "ease-in-out duration-500"
                    From: "opacity-100"
                    To: "opacity-0"
                -->
                <div class="absolute top-0 left-12 -ml-8 pt-4 pr-2 flex sm:-ml-10 sm:pr-4">
                <button id="close" type="button" class="rounded-md text-red-300 hover:text-white focus:outline-none focus:ring-2 focus:ring-white">
                    <span class="sr-only">Đóng</span>
                    <!-- Heroicon name: outline/x -->
                    <svg class="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor" aria-hidden="true">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
                </div>

                <div class="h-full flex flex-col py-6 bg-white shadow-xl overflow-y-scroll">
                <div class="px-4 sm:px-6">
                    <h2 class="text-lg font-medium text-gray-900" id="slide-over-title">
                    Thông tin khí tượng thủy văn
                    </h2>
                </div>
                <div class="mt-6 relative flex-1">
                    <!-- Replace with your content -->
                    <div id="vis"></div>
                    <div id="city-info"></div>
                    <!-- /End replace -->
                </div>
                </div>
            </div>
            </div>
        </div>
        </div>
        '''
        self.map.get_root().html.add_child(Element(html_body))

    