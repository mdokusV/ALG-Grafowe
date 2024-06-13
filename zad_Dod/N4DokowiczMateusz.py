import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


def read_matrix(filename):
    with open(filename, "r") as file:
        matrix = [list(map(int, line.split())) for line in file]
    return matrix


def create_graph(matrix):
    G = nx.Graph()
    rows, cols = len(matrix), len(matrix[0])
    for i in range(rows):
        for j in range(cols):
            if matrix[i][j] == 1:
                G.add_node((i, j))
                if i + 1 < rows and matrix[i + 1][j] == 1:
                    G.add_edge((i, j), (i + 1, j))
                if j + 1 < cols and matrix[i][j + 1] == 1:
                    G.add_edge((i, j), (i, j + 1))
    return G


def draw_graph(G, matching):
    pos = {node: (node[1], -node[0]) for node in G.nodes()}
    plt.figure(figsize=(10, 10))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=500,
        font_size=8,
        font_weight="bold",
    )
    matching_edges = [(u, v) for u, v in matching]
    nx.draw_networkx_edges(G, pos, edgelist=matching_edges, edge_color="red", width=2.0)
    plt.title("Graf pokrycia domina")
    plt.show()


filename = "N4.txt"
matrix = read_matrix(filename)
G = create_graph(matrix)

matching = nx.max_weight_matching(G, maxcardinality=True)

if len(matching) * 2 == len(G.nodes()):
    print("Pokrycie jest możliwe.")
else:
    print("Pokrycie nie jest możliwe. Pokazano największe możliwe skojarzenie.")

draw_graph(G, matching)
