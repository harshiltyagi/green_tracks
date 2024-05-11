import osmnx as ox
import networkx as nx
import folium
import random

# Define the OSM file path (You should provide your own OSM file).
osm_file_path = 'map.osm'

# Load the OSM data from the file
graph = ox.graph_from_xml(osm_file_path, simplify=False)

# Get a list of all nodes in the OSM data
all_nodes = list(graph.nodes)

# Choose two random nodes from the list
origin_node = random.choice(all_nodes)
target_node = random.choice(all_nodes)

# Calculate the shortest path using Dijkstra's algorithm
shortest_path = nx.shortest_path(graph, origin_node, target_node, weight='length')

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
