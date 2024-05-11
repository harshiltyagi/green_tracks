import osmnx as ox
import networkx as nx
import folium
import random
import pickle

# Define the OSM file path (You should provide your own OSM file).
osm_file_path = 'map.osm'

# Load the OSM data from the file
graph = ox.graph_from_xml(osm_file_path, simplify=False)

# Check if AQI and safety values already exist in the graph
if 'aqi_value' not in list(graph.edges[list(graph.edges.keys())[0]]):
    # Generate random AQI and safety values for the edges
    for edge in graph.edges:
        graph.edges[edge]['aqi_value'] = random.uniform(0, 100)  # Random AQI value between 0 and 100
        graph.edges[edge]['safety_score'] = random.uniform(0, 10)  # Random safety score between 0 and 10

    # Save the graph with the AQI and safety values to a file (if needed)
    with open('graph_with_aqi_safety.pickle', 'wb') as file:
        pickle.dump(graph, file)