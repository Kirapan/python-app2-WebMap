import folium
import pandas

data = pandas.read_csv("app2-web-map/Volcanoes_USA.txt")

lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
html = """
<h4>%s</h4>
%s m
"""

def color_producer(el):
  if el < 2000:
    return "green"
  elif 2000 <= el < 3000:
    return "orange"
  else:
    return "red"

map = folium.Map(location=[38.58, -99.12], zoom_start=4, tiles="Mapbox Bright")

fgp =  folium.FeatureGroup(name="Population")
fgp.add_child(folium.GeoJson(data=open("app2-web-map/world.json","r",encoding='UTF-8-sig').read(), 
style_function=lambda x: {'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else "orange" if 10000000 <= x['properties']['POP2005'] <= 20000000 else "red"}))

fgv =  folium.FeatureGroup(name="Volcanoes")
for la, lo, el, na in zip(lat, lon, elev, name):
  iframe = folium.IFrame(html=html % (str(na), str(el)), width=200,height=100)
  fgv.add_child(folium.CircleMarker(location=[la, lo], radius=6, popup=folium.Popup(iframe), color="grey",fill=True, fill_color=color_producer(el), fill_opacity=0.7))

map.add_child(fgp)
map.add_child(fgv)
map.add_child(folium.LayerControl())
map.save("map.html")