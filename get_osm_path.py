import osmnx as ox
import networkx as nx
import folium
import random
from geopy.distance import geodesic

# Specify the path to your OSM file or use an OSM extract
osm_file_path = "map.osm"

# Load the OSM data from the file
G = ox.graph_from_xml(osm_file_path, simplify=False)

# Randomly select a starting point
start_node = random.choice(list(G.nodes()))
# Ensure the starting node is on the road network
start_node = ox.distance.nearest_nodes(G, X=G.nodes[start_node]['x'], Y=G.nodes[start_node]['y'])

# Randomly select an ending point
end_node = random.choice(list(G.nodes()))
# Ensure the ending node is on the road network
end_node = ox.distance.nearest_nodes(G, X=G.nodes[end_node]['x'], Y=G.nodes[end_node]['y'])

# Get the latitude and longitude of the selected nodes
latitude_start = G.nodes[start_node]['y']
longitude_start = G.nodes[start_node]['x']
latitude_end = G.nodes[end_node]['y']
longitude_end = G.nodes[end_node]['x']

# Assign random AQI and safety values to edges (not nodes)
for u, v, k, data in G.edges(keys=True, data=True):
    G[u][v][k]['AQI'] = random.randint(1, 100)  # Assign a random AQI value between 1 and 100
    G[u][v][k]['Safety'] = random.uniform(0, 1)  # Assign a random safety value between 0 and 1

# Define a function to calculate the path cost based on AQI and safety
def path_cost_function(u, v, data):
    aqi = data.get('AQI', 0)  # Get the AQI attribute or use 0 if it doesn't exist
    safety = data.get('Safety', 1)  # Get the Safety attribute or use 1 if it doesn't exist

    start_node = G.nodes[u]
    end_node = G.nodes[v]
    # Calculate the edge length based on the geographic coordinates
    edge_length = geodesic((start_node['y'], start_node['x']), (end_node['y'], end_node['x'])).m

    return edge_length + (100 - aqi) + (1 - safety)

# Calculate the shortest path using bidirectional Dijkstra
shortest_path = nx.bidirectional_dijkstra(G, start_node, end_node, weight=path_cost_function)

# Extract the node coordinates and attributes of the locations in the shortest path
path_information = []
for u, v in zip(shortest_path, shortest_path[1:]):
    edge_attrs = G.get_edge_data(u, v)
    if edge_attrs:
        aqi = edge_attrs[0].get('AQI', 0)
        safety = edge_attrs[0].get('Safety', 1)
        path_information.append({'Latitude': G.nodes[v]['y'], 'Longitude': G.nodes[v]['x'], 'AQI': aqi, 'Safety': safety})

# Check if path_information is not empty before calculating map_center
if not path_information:
    raise ValueError("Path information is empty.")

# Calculate the map center based on path_information
map_center = [sum([coord['Latitude'] for coord in path_information])/len(path_information),
              sum([coord['Longitude'] for coord in path_information])/len(path_information)]

# Create a Folium map
m = folium.Map(location=map_center, zoom_start=15)

# Check if path_information is not empty before creating the PolyLine
if path_information:
    # Add markers for the locations in the path with AQI and safety attributes
    for location in path_information:
        latitude = location['Latitude']
        longitude = location['Longitude']
        aqi = location['AQI']
        safety = location['Safety']
        popup_text = f"AQI: {aqi}, Safety: {safety}"
        folium.Marker([latitude, longitude], popup=popup_text).add_to(m)

    # Add a polyline to represent the path
    path_coords = [(coord['Latitude'], coord['Longitude']) for coord in path_information]
    folium.PolyLine(path_coords, color="blue", weight=5).add_to(m)

# Display the map
m.save("path_map.html")
