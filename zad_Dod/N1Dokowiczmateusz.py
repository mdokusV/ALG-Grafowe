import networkx as nx
import matplotlib.pyplot as plt


def are_neighbors(word1, word2):
    return (word1[0] == word2[0]) or (word1[1] == word2[1]) or (word1[2] == word2[2])


def read_words(filename):
    with open(filename, "r") as file:
        words = file.read().strip().split()
    return words


def create_graph(words):
    G = nx.Graph()
    G.add_nodes_from(words)
    for i, word1 in enumerate(words):
        for j in range(i + 1, len(words)):
            word2 = words[j]
            if are_neighbors(word1, word2):
                G.add_edge(word1, word2)
    return G


def draw_graph_with_matching(G, matching):
    pos = nx.spring_layout(G)
    plt.figure(figsize=(12, 8))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        edge_color="gray",
        node_size=3000,
        font_size=10,
        font_weight="bold",
    )

    matching_edges = [(u, v) for u, v in matching]
    nx.draw_networkx_edges(G, pos, edgelist=matching_edges, edge_color="red", width=2.0)

    plt.title("Graf słów z największym skojarzeniem")
    plt.show()


filename = "N1.txt"
words = read_words(filename)
G = create_graph(words)

matching = nx.max_weight_matching(G, maxcardinality=True)

draw_graph_with_matching(G, matching)
