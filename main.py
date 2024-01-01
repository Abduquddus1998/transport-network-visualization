import networkx as nx  # python library to create Graph
import matplotlib.pyplot as plt  # python library to plot
# importing network_data
from network_data import network_dict, edge_colors, network_line_labels, edge_weights

# nx class initialization
network_graph = nx.Graph()
# setting plot size
plt.figure(figsize=(8, 8))


def add_network_nodes():
    # loops over is line of network_dict using iter function
    for line in iter(network_dict):
        # gets current dict
        network_line = network_dict[line]

        # each line consist of station(nodes) which stores details of the node
        for station in network_line:
            # adding node to the initialized Graph
            network_graph.add_node(station["short_name"], pos=station["pos"], color=station["color"])

            # if station has label_pos property then plot it
            if station["label_pos"]:
                x, y = station["label_pos"]  # gets coordinates, it is stored as a tuple
                plt.text(x, y, s=station["name"], rotation=0, fontsize=5, color=station["color"])


add_network_nodes()


# gets short names of the nodes and returns it weight
def get_edge_weight(from_none, to_node):
    # loops over edge_weights array
    for edge_weight in iter(edge_weights):

        # finds right edge dictionary and returns weight property
        if from_none == edge_weight["from"] and to_node == edge_weight["to"]:
            return edge_weight["weight"]

    return 0


def add_network_edges():
    # loops over network_dict
    for line in iter(network_dict):
        # get current line
        network_line = network_dict[line]
        # get color for specific line
        line_color = edge_colors[line]

        # loops over each node of the line and connects each of them
        for i in range(0, len(network_line) - 1):
            next_node = i + 1

            current_node = network_line[i]  # current node
            next_node = network_line[next_node]  # next node

            # gets edge weight between current and next node.
            weight = get_edge_weight(current_node["short_name"], next_node["short_name"])

            # adds edge between current and next node with given color and weight
            network_graph.add_edge(current_node["short_name"], next_node["short_name"], color=line_color, weight=weight)


add_network_edges()

# gets position attribute from node
pos = nx.get_node_attributes(network_graph, 'pos')
# gets color attribute from node
node_color = nx.get_node_attributes(network_graph, 'color')
# gets color attribute from edge
edge_color = nx.get_edge_attributes(network_graph, 'color')

# converts value of attributes to the list
node_color_list = list(node_color.values())
edge_color_list = list(edge_color.values())

# Node styles
options = {
    "font_size": 8,
    "node_size": 300,
    "font_color": "#fff"
}

# draws graph nodes
nx.draw_networkx(network_graph, pos, node_color=node_color_list, **options)
# draws graph edges
nx.draw_networkx_edges(network_graph, pos, edge_color=edge_color_list, width=4)


# adds each network line name to the graph
def add_edge_labels():
    # iterates over network line labels array
    for line in iter(network_line_labels):
        x, y = line["pos"]  # gets label position

        # draws network label witch given name and color
        plt.text(x, y, s=line["name"], rotation=0, fontsize=10, color=line["color"])


# function call
add_edge_labels()

# gets edge weight attribute
edge_labels = nx.get_edge_attributes(network_graph, "weight")

# draws graph edge labels in our case it is weight
nx.draw_networkx_edge_labels(network_graph, pos, edge_labels, font_size=6)

# Sets title for plot
plt.title("Stockholm metro network")
# Description for edge weight
plt.text(95, -92, 'Distances between edges represented in kilometres', fontsize=8)
# Shows graph
plt.show()
