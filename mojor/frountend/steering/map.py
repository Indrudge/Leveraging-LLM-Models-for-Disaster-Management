import osmnx as ox
import folium
from shapely.geometry import MultiPolygon, Polygon
from django.conf import settings
import os

def generate_map(location):
    """
    Generates a map for the given location, highlighting boundaries and hospitals.
    Saves the map as an HTML file and returns the file path.
    """
    try:
        # Retrieve boundary and hospitals for the given location
        boundary = ox.geocode_to_gdf(location)
        tags = {'amenity': 'hospital'}
        hospitals = ox.features_from_place(location, tags)
        
        # Create a Folium map centered on the location
        map_center = boundary.geometry.centroid.iloc[0].y, boundary.geometry.centroid.iloc[0].x
        mymap = folium.Map(location=map_center, zoom_start=10)

        # Plot boundary on the map
        for _, row in boundary.iterrows():
            geom = row['geometry']
            if isinstance(geom, MultiPolygon):
                for poly in geom.geoms:
                    boundary_coords = [(coord[1], coord[0]) for coord in poly.exterior.coords]
                    folium.Polygon(
                        locations=boundary_coords,
                        color="blue",
                        weight=2.5,
                        fill=True,
                        fill_opacity=0.2,
                        tooltip=f"Boundary of {location}"
                    ).add_to(mymap)
            elif isinstance(geom, Polygon):
                boundary_coords = [(coord[1], coord[0]) for coord in geom.exterior.coords]
                folium.Polygon(
                    locations=boundary_coords,
                    color="blue",
                    weight=2.5,
                    fill=True,
                    fill_opacity=0.2,
                    tooltip=f"Boundary of {location}"
                ).add_to(mymap)

        # Plot hospitals on the map with names and links to Google Maps
        for _, row in hospitals.iterrows():
            if hasattr(row.geometry, "x") and hasattr(row.geometry, "y"):
                hospital_name = row.get('name', 'Unknown Hospital')  # Get the name of the hospital or default
                latitude, longitude = row.geometry.y, row.geometry.x

                # Construct a Google Maps link for navigation
                google_maps_url = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

                # Add a marker with a clickable popup
                folium.Marker(
                    location=(latitude, longitude),
                    popup=folium.Popup(
                        f"<b>{hospital_name}</b><br><a href='{google_maps_url}' target='_blank'>Navigate</a>",
                        max_width=250
                    ),
                    icon=folium.Icon(color="red", icon="plus", prefix='fa')
                ).add_to(mymap)

        # Save the map to an HTML file
        map_dir = os.path.join(settings.BASE_DIR, 'templates', 'maps')
        os.makedirs(map_dir, exist_ok=True)
        map_path = os.path.join(map_dir, f"map.html")
        mymap.save(map_path)

        return f"maps/map.html"

    except Exception as e:
        print(f"Error generating map for {location}: {e}")
        return None
