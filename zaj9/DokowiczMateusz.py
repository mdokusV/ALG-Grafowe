from enum import Enum
from queue import Queue


class Group(Enum):
    UNKNOWN = 0
    GROUP1 = 1
    GROUP2 = 2

    def opposite(self):
        return Group.GROUP1 if self == Group.GROUP2 else Group.GROUP2


class Vertex:
    def __init__(self, index: int):
        self.index = index
        self.group = Group.UNKNOWN
        self.connects: list[Vertex] = []
        self.degree = 0
        self.pair: Vertex | None = None
        self.potential_predecessor: Vertex | None = None

    def add_connect(self, vertex: "Vertex", group: Group):
        self.connects.append(vertex)
        self.group = group
        self.degree += 1

    def __str__(self) -> str:
        return f"[{self.index}] group: {self.group}, degree: {self.degree}, connects:{[(vert.index, vert.group.name) for vert in self.connects]}"


class Vertices:

    def __init__(self, vertices_one: list[Vertex], vertices_two: list[Vertex]):
        self.vertex_one_group = vertices_one
        self.vertex_two_group = vertices_two
        self.coupling: dict[Vertex, Vertex] = {}

    def find_coupling(self) -> bool:
        for vertex in self.vertex_one_group:
            vert_to_check: Queue[Vertex] = Queue()
            vert_checked: list[Vertex] = []
            visited: set[Vertex] = set()
            vert_checked.append(vertex)
            vert_to_check.put(vertex)
            found_coupling = False
            while True:
                if found_coupling:
                    print(
                        "aktualne skojarzenie: ",
                        sorted(
                            [
                                (vert[1].index + 1, vert[0].index + 1)
                                for vert in self.coupling.items()
                            ]
                        ),
                    )
                    break
                if vert_to_check.empty():
                    print("nie znaleziono skojarzenia")
                    print(
                        f"S = {tuple(sorted([vert.index + 1 for vert in vert_checked]))}"
                    )
                    return False
                vert_current = vert_to_check.get()
                for successor in (v for v in vert_current.connects if v not in visited):
                    successor.potential_predecessor = vert_current
                    if successor.pair == None:
                        found_coupling = True
                        self.extend(successor)
                        break
                    else:
                        visited.add(successor)
                        vert_to_check.put(successor.pair)
                        vert_checked.append(successor.pair)

        return True

    def extend(self, vertex: Vertex):
        prev_vertex = vertex.potential_predecessor
        if prev_vertex == None:
            raise ValueError("Vertex has no potential predecessor")
        self.coupling[vertex] = prev_vertex
        print(f"{prev_vertex.index+1} {vertex.index+1}", end=" ")
        if prev_vertex.pair == None:
            vertex.pair = prev_vertex
            prev_vertex.pair = vertex
            print()
            return
        self.extend(prev_vertex.pair)
        vertex.pair = prev_vertex

    def __str__(self) -> str:
        return "".join(
            [
                str(vertex) + "\n"
                for vertex in self.vertex_one_group + self.vertex_two_group
            ]
        )


with open("graph11.txt", "r") as file:

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


vertices_group1 = [Vertex(i) for i in range(len(graph))]
vertices_group2 = [Vertex(i) for i in range(len(graph))]

vertices = Vertices(vertices_group1, vertices_group2)

for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i][j] == 1:
            vertices_group1[j].add_connect(vertices_group2[i], Group.GROUP1)
            vertices_group2[i].add_connect(vertices_group1[j], Group.GROUP2)


vertices.find_coupling()
