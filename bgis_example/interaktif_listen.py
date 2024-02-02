import bgis
from ipywidgets import Label
from ipyleaflet import Marker

Map = bgis.mapping(center=(40, -100), zoom=4)
label = Label()
coordinates = []


def handle_interaction(**kwargs):
    latlon = kwargs.get("coordinates")
    if kwargs.get("type") == "mousemove":
        label.value = str(latlon)
    elif kwargs.get("type") == "click":
        coordinates.append(latlon)
        Map.add_layer(Marker(location=latlon))


Map.listening(event="click", add_marker=True)
print(Map.last_click)
