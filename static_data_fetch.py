import osmnx as ox

# Specify the path to the OSM file
osm_file_path = "map.osm"

# Load the OSM data from the file
G = ox.graph_from_xml(osm_file_path, simplify=False)

# Extract all nodes from the graph
nodes = list(G.nodes(data=True))

# Print the coordinates of each node
for node in nodes:
    node_id, data = node
    latitude = data['y']
    longitude = data['x']
    print(f"Node {node_id}: Latitude {latitude}, Longitude {longitude}")
