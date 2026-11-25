"""Base binary tree drawing code (from task 4), shared by tasks 4 and 5."""

import uuid

import matplotlib.pyplot as plt
import networkx as nx


class Node:
    def __init__(self, key, color="skyblue"):
        self.left = None
        self.right = None
        self.val = key
        self.color = color  # node color
        self.id = str(uuid.uuid4())  # unique node identifier


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is not None:
        graph.add_node(node.id, color=node.color, label=node.val)
        if node.left:
            graph.add_edge(node.id, node.left.id)
            l = x - 1 / 2 ** layer
            pos[node.left.id] = (l, y - 1)
            add_edges(graph, node.left, pos, x=l, y=y - 1, layer=layer + 1)
        if node.right:
            graph.add_edge(node.id, node.right.id)
            r = x + 1 / 2 ** layer
            pos[node.right.id] = (r, y - 1)
            add_edges(graph, node.right, pos, x=r, y=y - 1, layer=layer + 1)
    return graph


def draw_tree(tree_root, title=None, ax=None, node_size=2500):
    """Draw the tree. If `ax` is given, draw into it (without plt.show)."""
    tree = nx.DiGraph()
    pos = {tree_root.id: (0, 0)}
    tree = add_edges(tree, tree_root, pos)

    colors = [node[1]["color"] for node in tree.nodes(data=True)]
    labels = {node[0]: node[1]["label"] for node in tree.nodes(data=True)}

    own_figure = ax is None
    if own_figure:
        plt.figure(figsize=(8, 5))
        ax = plt.gca()
    nx.draw(tree, pos=pos, labels=labels, arrows=False, node_size=node_size,
            node_color=colors, ax=ax, font_color="white", font_weight="bold")
    if title:
        ax.set_title(title)
    if own_figure:
        plt.show()
