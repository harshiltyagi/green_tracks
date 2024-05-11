import folium
import networkx as nx
import pickle
import random

# Load the graph from the pickled file
with open("graph_with_aqi_safety.gpickle", "rb") as file:
    graph = pickle.load(file)

# Choose the number of nodes you want to display
num_nodes_to_display = 50  # Adjust this number as needed

# Randomly select nodes from the graph
random_nodes = random.sample(graph.nodes, num_nodes_to_display)

# Create a Folium map
m = folium.Map(location=[latitude, longitude], zoom_start=12)

# Add markers for the randomly selected nodes on the map
for node in random_nodes:
    node_data = graph.nodes[node]
    folium.Marker(
        location=[node_data['latitude'], node_data['longitude']],
        popup=node_data['label']
    ).add_to(m)

# Save the map as an HTML file
m.save('random_city_map.html')
