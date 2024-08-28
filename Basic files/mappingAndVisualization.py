import folium

def create_map(locations):
    m = folium.Map(location=[locations[0]['lat'], locations[0]['lng']], zoom_start=10)
    for location in locations:
        folium.Marker([location['lat'], location['lng']], popup=location['name']).add_to(m)
    m.save('map.html')