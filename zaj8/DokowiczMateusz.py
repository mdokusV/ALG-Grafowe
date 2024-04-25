from pprint import pprint


class Tree:

    def __init__(self, root: int, children: list[int]):
        self.children = children

    def __hash__(self) -> int:
        return hash(tuple(self.children))

    def __eq__(self, other) -> bool:
        return self.children == other.children

    def __str__(self) -> str:
        return f"children: {self.children}"


class Vertex:
    def __init__(self, index: int):
        self.index = index
        self.connects: list[Vertex] = []
        self.free_children: dict[int, Vertex] = {}
        self.degree = 0

    def __str__(self):
        return f"[{self.index}] degree: {self.degree}, connects:{[vert.index for vert in self.connects]}"

    def remove_child(self):
        for vert in self.connects:  # TODO: maybe change it to self.free_children
            if self.index in vert.free_children:
                vert.free_children.pop(self.index)

    def add_child(self):
        for vert in self.connects:
            vert.free_children[self.index] = self


def get_permutation(items: list[Vertex], n: int):
    binary_list = [not ((bool(int(i)))) for i in list(bin(n)[2:].zfill(len(items)))]
    return [items[i] for i, v in enumerate(binary_list) if v == True]


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex_list = vertices
        self.tree_cache = {}
        self.unmarked_vertices: set[Vertex] = set(self.vertex_list)
        self.waiting_to_check: list[Vertex] = []
        self.number_of_trees = 0

    def __str__(self):
        return "".join([str(vertex) + "\n" for vertex in self.vertex_list])

    def dfs(self, vertex: Vertex):
        print(vertex)
        permutation_number = 0
        permutation = get_permutation(
            list(vertex.free_children.values()), permutation_number
        )
        while len(permutation) >= len(vertex.free_children):
            self.add_children_from_permutation(permutation)
            if len(self.waiting_to_check) == 0:
                if len(self.unmarked_vertices) == 0:
                    self.number_of_trees += 1
                self.reverse_add_children_from_permutation(permutation)
                return
            next_vertex = self.waiting_to_check.pop()
            self.dfs(next_vertex)
            permutation_number -= 1
            permutation = get_permutation(
                list(vertex.free_children.values()), permutation_number
            )
            self.reverse_add_children_from_permutation(permutation)

    def add_children_from_permutation(self, permutation: list[Vertex]):
        for child in permutation:
            if child in self.unmarked_vertices:
                self.waiting_to_check.append(child)
                self.unmarked_vertices.remove(child)
                child.remove_child()

    def reverse_add_children_from_permutation(self, permutation: list[Vertex]):
        for child in permutation:
            if child in self.unmarked_vertices:
                self.unmarked_vertices.add(child)
                child.add_child()


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
vertices.dfs(initial_root)
print(vertices.number_of_trees)
