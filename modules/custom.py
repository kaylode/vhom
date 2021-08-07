import folium
from jinja2 import Template


class OnClickMarker(folium.Marker):
    def __init__(self, location=None, popup=None, tooltip=None, icon=None,
                 draggable=False, on_click=None, **kwargs):
        super().__init__(location=location, popup=popup, tooltip=tooltip, icon=icon, draggable=draggable, **kwargs)
        self.on_click = on_click

        self._template = Template(u"""
        {% macro script(this, kwargs) %}
            var {{ this.get_name() }} = L.marker(
                {{ this.location|tojson }},
                {{ this.options|tojson }}
            ).addTo({{ this._parent.get_name() }}).on('click',{{ this.on_click }});
        {% endmacro %}
        """)
    