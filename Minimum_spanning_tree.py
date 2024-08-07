import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import distance

class GRAPH_CUSTOM:
    def __init__(self, attrs=None, graph=None):
        if attrs is not None:
            self.graph = self.graph_constructor(attrs)
        elif graph is not None:
            self.graph = graph
        else:
            raise ValueError("Either attrs or graph must be provided")

    def graph_constructor(self, attrs):
        G = nx.Graph()

        # Adding nodes with attributes
        for key, values in attrs.items():
            node_type = values["obj_type"]
            node_color = 'black' if node_type == "House" else 'red'
            G.add_node(key, type=node_type, color=node_color, coordinates=values["coordinates"])

        # Adding edges with attributes
        weight = 0.1
        for key_i, values_i in attrs.items():
            for key_j, values_j in attrs.items():
                if key_i != key_j:
                    dist = distance.euclidean(values_i["coordinates"], values_j["coordinates"])
                    if (values_i["obj_type"] == "House" and values_j["obj_type"] == "House") or \
                    (values_i["obj_type"] == "Mall" and values_j["obj_type"] == "House") or \
                    (values_i["obj_type"] == "House" and values_j["obj_type"] == "Mall"):
                        edge_type = "slow"
                        edge_color = 'black'
                        edge_weight = dist * weight
                        G.add_edge(key_i, key_j, weight=edge_weight, type=edge_type, color=edge_color)
                    elif (values_i["obj_type"] == "Mall" and values_j["obj_type"] == "Mall") or \
                        (values_i["obj_type"] == "Mall" and values_j["obj_type"] == "Center") or \
                        (values_i["obj_type"] == "Center" and values_j["obj_type"] == "Mall"):
                        edge_type = "fast"
                        edge_color = 'red'
                        edge_weight = dist * (1 - weight)
                        G.add_edge(key_i, key_j, weight=edge_weight, type=edge_type, color=edge_color)
                    else:
                        continue  # Skip edges that don't match any condition

        return G

    def MST(self):
        mst = self.prim_algorithm(self.graph)
        return GRAPH_CUSTOM(graph=mst)

    def prim_algorithm(self, graph):
        nodes = graph.nodes(data=True)
        mst = nx.Graph()
        mst.add_nodes_from(nodes)

        not_visited = set(graph.nodes())
        start = list(graph.nodes())[0]
        visited = {start}
        not_visited.remove(start)

        while not_visited:
            min_weight = float('inf')
            min_edge = None
            
            for u in visited:
                for v in set(graph[u]) & not_visited:
                    weight = graph[u][v]['weight']

                    if weight < min_weight:
                        min_weight = weight
                        min_edge = (u, v)

            if min_edge is None:
                break
            
            u, v = min_edge

            mst.add_edge(u, v, **graph[u][v])

            visited.add(v)
            not_visited.remove(v)

        return mst

    def graph_vis(self):
        title = "Minimum Spanning Tree" if self.graph.number_of_edges() < self.graph.number_of_nodes() else "Full Graph"
        self._visualize_graph(self.graph, f"{title} of Houses, Malls, and Centers")

    def _visualize_graph(self, graph, title):
        plt.figure(figsize=(10, 8))

        # Get positions from node attributes
        pos = nx.get_node_attributes(graph, 'coordinates')

        # Get node colors from node attributes
        node_colors = [graph.nodes[node]['color'] for node in graph.nodes()]

        # Get edge colors from edge attributes
        edge_colors = [graph[u][v]['color'] for u, v in graph.edges()]

        # Draw nodes
        nx.draw_networkx_nodes(graph, pos, node_color=node_colors, node_size=700)

        # Draw edges
        nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)

        # Draw labels
        nx.draw_networkx_labels(graph, pos, font_size=10, font_color='white')

        # Draw edge labels (weights)
        edge_labels = {(u, v): f"{d['weight']:.2f}" for u, v, d in graph.edges(data=True)}
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_color='blue')

        plt.title(title)
        plt.axis('off')
        plt.tight_layout()
        plt.show()

        total_slow = sum(d['weight'] for _, _, d in graph.edges(data=True) if d['type'] == 'slow')
        total_fast = sum(d['weight'] for _, _, d in graph.edges(data=True) if d['type'] == 'fast')

        print(f"Total weight of slow edges: {total_slow:.2f}")
        print(f"Total weight of fast edges: {total_fast:.2f}")

attrs = {0: {"obj_type": 'House', "coordinates": (1,2)},
        1: {"obj_type": 'Mall', "coordinates": (2,3)},
        2: {"obj_type": 'House', "coordinates": (1,3)},
        3: {"obj_type": 'House', "coordinates": (1,4)},
        4: {"obj_type": 'Mall', "coordinates": (3,3)},
        5: {"obj_type": 'House', "coordinates": (2,4)},
        6: {"obj_type": 'Center', "coordinates": (3,5)},
        7: {"obj_type": 'House', "coordinates": (1,2)},
        8: {"obj_type": 'Mall', "coordinates": (5,3)},
        9: {"obj_type": 'House', "coordinates": (3,7)},
        10: {"obj_type": 'House', "coordinates": (1,1)},
        11: {"obj_type": 'Mall', "coordinates": (1,5)},
        12: {"obj_type": 'House', "coordinates": (2,2)},
        13: {"obj_type": 'House', "coordinates": (4,4)}}

if __name__ == "__main__":
    tree = GRAPH_CUSTOM(attrs)
    mst = tree.MST()
    mst.graph_vis()
