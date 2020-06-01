import folium
import pandas

map = folium.Map(location=[38.58, -99.09], zoom_start=5, tiles="CartoDB Positron")

data = pandas.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
name = list(data["NAME"])
el = list(data["ELEV"])

def color_points(el):
    if el < 1000:
        return 'red'
    elif 1000<= el < 3000:
        return 'green'
    else:
        return 'blue'

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Elevation: %sm
"""
#feature group useful, else all volcanoes will need to be added as individual children/layers
fgv = folium.FeatureGroup(name="USA Volcanoes")

#adding (JS) Leaflet markers, popup optional
for lt, ln, name, el in zip(lat, lon, name, el):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=7, popup=folium.Popup(iframe), fill_color=color_points(el),
                                     color='black', fill_opacity=1))

fgp = folium.FeatureGroup(name="Population")

fgp.add_child(folium.GeoJson(data=open("world.json", encoding="utf-8-sig").read(),
                            style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000
                                                      else 'yellow' if 10000000 <= x['properties']['POP2005'] < 20000000
                                                      else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
#must be added after feature groups, else the layers will be missing
map.add_child(folium.LayerControl())

map.save("Map1.html")