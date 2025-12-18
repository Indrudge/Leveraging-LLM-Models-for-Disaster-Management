# Import required libraries
import osmnx as ox
import folium
from shapely.geometry import Point, MultiPolygon, Polygon
import os
from django.conf import settings

# Define multiple locations
locations = [
    "Jaipur", "Dausa", "Jhunjhunu", "Sawai Madhopur", "Sriganganagar", 
    "Rajsamand", "Sikar", "Pratapgarh", "Jalore", "Sirohi", 
    "Bharatpur", "Barmer", "Dholpur", "Hanumangarh", "Udaipur", 
    "Bundi", "Jhalawar", "Baran"
]

# Initialize the Folium map (centered on India)
map_center = [20.5937, 78.9629]  # Centered on India
mymap = folium.Map(location=map_center, zoom_start=5)

# Function to retrieve boundary and hospitals for a location
def get_boundary_and_hospitals(location_name):
    # Download the boundary polygon for the location
    boundary = ox.geocode_to_gdf(location_name)
    
    # Use OpenStreetMap tags to find hospitals within this area
    tags = {'amenity': 'hospital'}
    hospitals = ox.features_from_place(location_name, tags)
    
    return boundary, hospitals

# Loop through each location to add boundaries and hospitals to the map
for location_name in locations:
    try:
        # Get boundary and hospitals for the location
        boundary, hospitals = get_boundary_and_hospitals(location_name)
        
        # Plot the boundary on the map
        for _, row in boundary.iterrows():
            geom = row['geometry']
            if isinstance(geom, MultiPolygon):
                for poly in geom.geoms:  # Iterate through each Polygon in MultiPolygon
                    boundary_coords = [(coord[1], coord[0]) for coord in poly.exterior.coords]
                    folium.Polygon(
                        locations=boundary_coords, 
                        color="blue", 
                        weight=2.5, 
                        fill=True, 
                        fill_opacity=0.2, 
                        tooltip=f"Boundary of {location_name}"
                    ).add_to(mymap)
            elif isinstance(geom, Polygon):
                boundary_coords = [(coord[1], coord[0]) for coord in geom.exterior.coords]
                folium.Polygon(
                    locations=boundary_coords, 
                    color="blue", 
                    weight=2.5, 
                    fill=True, 
                    fill_opacity=0.2, 
                    tooltip=f"Boundary of {location_name}"
                ).add_to(mymap)

        # Plot each hospital within the boundary
        for _, row in hospitals.iterrows():
            if isinstance(row.geometry, Point):
                folium.Marker(
                    location=(row.geometry.y, row.geometry.x),
                    popup=f"Hospital in {location_name}",
                    icon=folium.Icon(color="red", icon="plus", prefix='fa')
                ).add_to(mymap)

    except Exception as e:
        print(f"Could not process {location_name} due to error: {e}")

impath = os.path.join(settings.TEMPLATES.DIRS)

# Save the map to an HTML file
mymap.save("multiple_locations_hospitals_map.html")
print("Map saved as multiple_locations_hospitals_map.html")
