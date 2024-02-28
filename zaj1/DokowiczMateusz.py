from pprint import pprint
from numpy import Inf

def change_type(str) -> float:
    if str == "-":
        return Inf
    return int(str)

with open("graph.txt", "r") as file:
    graph = []
    for line in file:
        line = line.split()
        line = [change_type(x) for x in line]
        graph.append(line)

def make_adj_matrix(graph) -> dict:
    n = len(graph)
    adj_matrix = {}
    for i in range(n):
        adj_matrix[i+1] = []
        for j in range(n):
            if graph[i][j] != Inf:
                adj_matrix[i+1].append(j+1)
    
    return adj_matrix

def make_adj_matrix_with_weights(graph) -> dict:
    n = len(graph)
    adj_matrix = {}
    for i in range(n):
        adj_matrix[i+1] = {}
        for j in range(n):
            if graph[i][j] != Inf:
                adj_matrix[i+1].update({j+1: graph[i][j]})

    return adj_matrix

def make_adj_edge_list_with_weights(graph) -> dict:
    n = len(graph)
    adj_matrix = {}
    for i in range(n):
        for j in range(n):
            if graph[i][j] != Inf:
                edge = tuple(sorted([i+1, j+1]))
                adj_matrix.update({edge: graph[i][j]})
    
    return adj_matrix

def edge_deg_sorted(graph: dict) -> list:
    degrees = []
    for i in graph:
        degrees.append(len(graph[i]))
    return sorted(degrees, reverse=True)

def number_of_edges(graph: dict) -> int:
    return len(graph)
    


print("\na:")
pprint(graph)

print("\nb:")
adj_matrix = make_adj_matrix(graph)
pprint(adj_matrix)

print("\nc:")
adj_matrix_weights = make_adj_matrix_with_weights(graph)
pprint(adj_matrix_weights)

print("\nd:")
adj_edge_list_with_weights = make_adj_edge_list_with_weights(graph)
pprint(adj_edge_list_with_weights)

print("\ne:")
pprint(adj_matrix)

print("\nf.a:")
edge_deg = edge_deg_sorted(adj_matrix)
pprint(edge_deg)

print("\nf.b:")
edge_deg = number_of_edges(adj_edge_list_with_weights)
pprint(edge_deg)



