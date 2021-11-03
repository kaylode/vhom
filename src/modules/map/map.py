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

        html_body = '''

        <!-- This example requires Tailwind CSS v2.0+ -->
        <nav class="bg-gradient-to-r from-green-400 to-blue-500 shadow-lg block">
			<div class="max-w-7xl mx-auto px-4">
				<div class="flex justify-between">
					<div class="flex space-x-16">
						<div>
							<!-- Website Logo -->
							<a href="#" class="flex items-center py-4 px-2 hover:no-underline">
								<img src="/web/static/assets/logo.png" alt="Logo" class="h-12 w-12 mr-2">
								<span class="font-semibold text-yellow-200 text-4xl">Khí tượng thủy văn Việt Nam</span>
							</a>
						</div>
						<!-- Primary Navbar items -->
						<div class="md:flex items-center space-x-16">
							<a href="#" class="py-4 px-2 text-green-300 border-b-4 border-green-500 font-semibold text-2xl">Trang chủ</a>
							<a href="#" class="py-4 px-2 text-white font-semibold hover:text-green-200 transition duration-300 text-2xl">Thông tin dự án</a>
							<a href="#" class="py-4 px-2 text-white font-semibold hover:text-green-200 transition duration-300 text-2xl">Liên hệ</a>
						</div>
					</div>
					<!-- Secondary Navbar items
					<div class="hidden md:flex items-center space-x-3 ">
						<a href="" class="py-2 px-2 font-medium text-gray-500 rounded hover:bg-green-500 hover:text-white transition duration-300">Log In</a>
						<a href="" class="py-2 px-2 font-medium text-white bg-green-500 rounded hover:bg-green-400 transition duration-300">Sign Up</a>
					</div> -->
				</div>
			</div>
		</nav>

        <div>

            <div id="city-info-box" class="info_float2 bg-red-100 ring ring-red-600 ring-offset-4 ring-offset-red-100">
                <p id="city-info" class="py-4">s</p>
            </div>

            <div id="weather-info-box" class="font-sans text-2xl text-center info_float bg-green-100 ring ring-green-600 ring-offset-4 ring-offset-green-100">
                <p id="date" class="pt-6"></p>
                <p id="time" class="py-2 text-5xl"></p>
            </div>
        </div>

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
            <div class="fixed inset-y-0 right-0 pl-10 max-w-full flex">
            <!--
                Slide-over panel, show/hide based on slide-over state.

                Entering: "transform transition ease-in-out duration-500 sm:duration-700"
                From: "translate-x-full"
                To: "translate-x-0"
                Leaving: "transform transition ease-in-out duration-500 sm:duration-700"
                From: "translate-x-0"
                To: "translate-x-full"
            -->
            <div id="sliding_anim" class="relative w-screen max-w-3xl border-l-2 border-black border-opacity-20 transform transition ease-in-out duration-500 sm:duration-700 translate-x-full" >
                <!--
                Close button, show/hide based on slide-over state.

                Entering: "ease-in-out duration-500"
                    From: "opacity-0"
                    To: "opacity-100"
                Leaving: "ease-in-out duration-500"
                    From: "opacity-100"
                    To: "opacity-0"
                -->
                <div class="rounded-l-3xl border-l-2 border-black border-opacity-50 bg-white absolute top-1/2 -left-1.5 -ml-8 flex sm:-ml-10 sm:pr-4">
                <button id="close" type="button" class="pl-2 h-20 w-6 rounded-xl text-red-200 hover:text-white focus:outline-none focus:ring-2 focus:ring-white">
                    <span class="sr-only">Đóng</span>
                    <img id="close_arrow" src="https://cdn-icons-png.flaticon.com/512/50/50621.png" alt="double_arrow" width="50" height="100">

                </button>
                </div>

                <div class="h-full flex flex-col bg-white shadow-xl overflow-y-scroll">
                <div class="bg-green-600 px-4 sm:px-6">
                    <h2 class="font-bold text-3xl font-sans font-large text-gray-900" id="slide-over-title">
                    Thông tin khí tượng thủy văn
                    </h2>
                </div>
                <div class="mt-6 relative flex-1 divide-y-4 divide-yellow-500">
                    <!-- Replace with your content -->
                    <div id="vis"></div>
                    <!--
                    <div id="statistic" class="text-9xl relative font-sans pt-10 grid grid-cols-3 gap-y-14">
                        <div id="min-level1">11cm</div>
                        <div id="max-level1">211cm</div>
                        <div id="avg-level1">3cm</div>

                        <div id="min-level2">4cm</div>
                        <div id="max-level2">5cm</div>
                        <div id="avg-level2">6cm</div>
                    </div> -->
                    <!-- /End replace -->
                </div>
                </div>
            </div>
            </div>
        </div>
        </div>
        '''
        self.map.get_root().html.add_child(Element(html_body))

    