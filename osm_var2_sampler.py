import osmnx as ox
import networkx as nx
import folium
import random

# Define the OSM file path (You should provide your own OSM file).
osm_file_path = 'map.osm'

# Load the OSM data from the file
graph = ox.graph_from_xml(osm_file_path, simplify=False)

# Generate random AQI and safety values for the edges
for edge in graph.edges:
    graph.edges[edge]['aqi_value'] = random.uniform(0, 100)  # Random AQI value between 0 and 100
    graph.edges[edge]['safety_score'] = random.uniform(0, 10)  # Random safety score between 0 and 10

# Get a list of all nodes in the OSM data
all_nodes = list(graph.nodes)

# Choose two random nodes from the list
origin_node = random.choice(all_nodes)
target_node = random.choice(all_nodes)

# Define weights for AQI and safety (customize as needed)
weight_aqi = 0.6  # Adjust the weight for AQI
weight_safety = 0.4  # Adjust the weight for safety

# Define a function to calculate edge weights based on AQI and safety
def recalculate_edge_weight(u, v, d):
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
m.save('random_shortest_path.html')
