import folium
from jinja2 import Template


class OnClickMarker(folium.Marker):
    def __init__(self, location=None, popup=None, tooltip=None, icon=None, 
                 draggable=False, on_click=None, on_click_data=None, **kwargs):
        super().__init__(location=location, popup=popup, tooltip=tooltip, icon=icon, draggable=draggable, **kwargs)
        self.on_click = on_click if on_click is not None else None
        self.on_click_data = on_click_data if on_click_data is not None else "{ }"
        
        if self.on_click is not None:
            self._template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{ this.get_name() }} = L.marker(
                    {{ this.location|tojson }},
                    {{ this.options|tojson }}
                ).addTo({{ this._parent.get_name() }}).on('click', function(e){ {{ this.on_click }} (e, {{ this.on_click_data }}) });
            {% endmacro %}
            """)
    
class CustomJavaScript(folium.JavascriptLink):
    def __init__(self, url, type=None, download=False):
        super().__init__(url, download=download)
        self.type = type

        if type is not None:
            self._template = Template(
                '{% if kwargs.get("embedded",False) %}'
                '<script>{{this.get_code()}}</script>'
                '{% else %}'
                '<script type="{{this.type}}" src="{{this.url}}"></script>'
                '{% endif %}'
            )