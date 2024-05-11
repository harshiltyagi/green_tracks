import osmnx as ox
import networkx as nx
import folium
import random
import pickle

# Define the OSM file path
osm_file_path = 'map.osm'

# Check if the saved graph file with AQI and safety values exists
try:
    with open('graph_with_aqi_safety.gpickle', 'rb') as file:
        graph = pickle.load(file)
except FileNotFoundError:
    # If the file doesn't exist, create a new graph with random values
    graph = ox.graph_from_xml(osm_file_path, simplify=False)
    for edge in graph.edges:
        graph.edges[edge]['aqi_value'] = random.uniform(0, 100)
        graph.edges[edge]['safety_score'] = random.uniform(0, 10)
    # Save the graph for future use
    with open('graph_with_aqi_safety.gpickle', 'wb') as file:
        pickle.dump(graph, file)

# Define source and target coordinates
origin_coords = (52.3637317, 4.8268779)  # Replace with your desired coordinates
target_coords = (52.358276, 4.8290307)   # Replace with your desired coordinates

# Find the nearest nodes to the specified coordinates
origin_node = ox.distance.nearest_nodes(graph, origin_coords[1], origin_coords[0])
target_node = ox.distance.nearest_nodes(graph, target_coords[1], target_coords[0])

# Define weights for AQI and safety
weight_aqi = 0.6
weight_safety = 0.4

# Define a function to calculate edge weights based on AQI and safety
def calculate_edge_weight(u, v, d):
    aqi_weight = weight_aqi * d.get('aqi_value', 0)  # Default to 0 if data is missing
    safety_weight = weight_safety * d.get('safety_score', 0)  # Default to 0 if data is missing
    total_weight = aqi_weight + safety_weight
    return total_weight

# Calculate the shortest path using the defined edge weight function
shortest_path = nx.shortest_path(graph, origin_node, target_node, weight=calculate_edge_weight)

# Get the coordinates of the origin and target nodes
origin_coords = (graph.nodes[origin_node]['y'], graph.nodes[origin_node]['x'])
target_coords = (graph.nodes[target_node]['y'], graph.nodes[target_node]['x'])

# Create a map centered on the origin node
m = folium.Map(location=origin_coords, zoom_start=14)

# Convert the networkx graph to a folium graph
gdf_nodes, gdf_edges = ox.graph_to_gdfs(graph)

# Create a list to store the coordinates of all nodes in the shortest path
shortest_path_coords = []

for node in shortest_path:
    node_coords = (graph.nodes[node]['y'], graph.nodes[node]['x'])
    shortest_path_coords.append(node_coords)

# Create a polyline for the entire path
folium.PolyLine(locations=shortest_path_coords, color='red').add_to(m)

# Add markers for the origin and target nodes
folium.Marker(location=origin_coords, icon=folium.Icon(color='green')).add_to(m)
folium.Marker(location=target_coords, icon=folium.Icon(color='purple')).add_to(m)

# Save the map to an HTML file
m.save('coordinate_based_shortest_path.html')
