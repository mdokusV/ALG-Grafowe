from pprint import pprint


class Tree:
    def __init__(self, root: int, children: list[int]):
        self.root = root
        self.children = children

    def __hash__(self) -> int:
        return hash((self.root, tuple(self.children)))

    def __eq__(self, other) -> bool:
        return self.root == other.root and self.children == other.children

    def __str__(self) -> str:
        return f"root: {self.root}, children: {self.children}"


class Vertex:
    def __init__(self, index: int):
        self.index = index
        self.connects: list[Vertex] = []
        self.free_children: dict[int, Vertex] = {}
        self.degree = 0

    def __str__(self):
        return f"[{self.index}] degree: {self.degree}, connects:{[vert.index for vert in self.connects]}"

    def remove_child(self):
        for vert in self.connects:
            if self.index in vert.free_children:
                vert.free_children.pop(self.index)


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex_list = vertices

    def __str__(self):
        return "".join([str(vertex) + "\n" for vertex in self.vertex_list])


tree_cache: dict[Tree, int] = {}

with open("Trees.txt", "r") as file:

    graph: list[list[int]] = []
    for line in file:
        items = line.split()
        row = []
        for i in items:
            if i == "-":
                row.append(0)
            else:
                row.append(int(i))
        graph.append(row)
pprint(graph)

vertices = Vertices([Vertex(i) for i in range(len(graph))])
for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i][j] == 1:
            vertices.vertex_list[i].connects.append(vertices.vertex_list[j])
            vertices.vertex_list[i].degree += 1
            vertices.vertex_list[i].free_children[j] = vertices.vertex_list[j]

print(vertices)

# DFS
initial_root = vertices.vertex_list[0]
from collections import deque

stack: deque[Vertex] = deque()
stack.append(initial_root)


def dfs(vertex: Vertex):
    vertex.remove_child()
    print(vertex)
    while vertex.free_children:
        child = vertex.free_children.popitem()[1]
        stack.append(child)
        dfs(child)


dfs(initial_root)
