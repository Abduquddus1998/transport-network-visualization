import networkx as nx
import matplotlib.pyplot as plt

from network_data import network_dict, edge_colors, network_line_labels, edge_weights

network_graph = nx.Graph()


def add_network_nodes():
    for line in iter(network_dict):
        network_line = network_dict[line]

        for station in network_line:
            network_graph.add_node(station["short_name"], pos=station["pos"], color=station["color"])

            if station["label_pos"]:
                x, y = station["label_pos"]
                plt.text(x, y, s=station["name"], rotation=0, fontsize=5, color=station["color"])


add_network_nodes()


def get_edge_weight(from_none, to_node):
    for edge_weight in iter(edge_weights):

        if from_none == edge_weight["from"] and to_node == edge_weight["to"]:
            return edge_weight["weight"]

    return 0


def add_network_edges():
    for line in iter(network_dict):
        network_line = network_dict[line]
        line_color = edge_colors[line]

        for i in range(0, len(network_line) - 1):
            next_node = i + 1

            current_node = network_line[i]
            next_node = network_line[next_node]

            weight = get_edge_weight(current_node["short_name"], next_node["short_name"])

            network_graph.add_edge(current_node["short_name"], next_node["short_name"], color=line_color, weight=weight)


add_network_edges()

pos = nx.get_node_attributes(network_graph, 'pos')
node_color = nx.get_node_attributes(network_graph, 'color')
edge_color = nx.get_edge_attributes(network_graph, 'color')

node_color_list = list(node_color.values())
edge_color_list = list(edge_color.values())


def add_edge_labels():
    for line in iter(network_line_labels):
        x, y = line["pos"]
        plt.text(x, y, s=line["name"], rotation=0, fontsize=10, color=line["color"])


add_edge_labels()

options = {
    "font_size": 8,
    "node_size": 300,
    "font_color": "#fff"
}

nx.draw_networkx(network_graph, pos, node_color=node_color_list, **options)
nx.draw_networkx_edges(network_graph, pos, edge_color=edge_color_list)

edge_labels = nx.get_edge_attributes(network_graph, "weight")
nx.draw_networkx_edge_labels(network_graph, pos, edge_labels, font_size=6)

plt.title("Stockholm metro map")
plt.text(70, -92, 'Distances between edges represented in kilometres', fontsize=8)

plt.show()
