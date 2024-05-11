import networkx as nx
import pickle
import matplotlib.pyplot as plt

# Load the graph from the pickled file
with open("graph_with_aqi_safety.gpickle", "rb") as file:
    graph = pickle.load(file)

# Adjust the layout and styling
pos = nx.spring_layout(graph, seed=42)  # You can adjust the seed for different layouts
node_size = 20
node_color = "skyblue"
edge_width = 0.2

# Draw the graph with improved settings
nx.draw_networkx_nodes(graph, pos, node_size=node_size, node_color=node_color)
nx.draw_networkx_edges(graph, pos, width=edge_width, alpha=0.5)
labels = {node: str(node) if len(str(node)) < 10 else "" for node in graph.nodes()}  # Label only short node names
nx.draw_networkx_labels(graph, pos, labels, font_size=7, font_color="black")

# Show the graph
plt.axis("off")
plt.show()
