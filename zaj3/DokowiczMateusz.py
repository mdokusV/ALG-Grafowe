from enum import Enum
from pprint import pprint


class Vertex:
    def __init__(self, successors: dict, predecessors: dict, index: int):
        self.successors: dict[int, Vertex] = successors
        self.predecessors: dict[int, Vertex] = predecessors
        self.index = index
        self.visited = False

    def __str__(self):
        return f"[{self.index}] successors:{list(self.successors.keys())}, predecessors:{list(self.predecessors.keys())}"


class Subgraph:
    def __init__(self, vertices: list[Vertex]):
        self.vertex = vertices
        self.reachability_matrix: list[list[list[int]]] = [[[], []], [[], []]]
        self.zero_deg_in: list[int] = []
        self.zero_deg_out: list[int] = []

    def __str__(self):
        matrix_info = ""
        for i, j in [(1, 1), (1, 0), (0, 1), (0, 0)]:
            matrix_info += f"V{i}{j}: {self.reachability_matrix[i][j]}\n"

        return f"{[vertex.index for vertex in self.vertex]}\n{matrix_info}\n"

    def reset_reachability_matrix(self):
        self.reachability_matrix = [[[], []], [[], []]]

    def init_zero_deg(self, zero_deg_in: list[int], zero_deg_out: list[int]):
        omega = set([i.index for i in self.vertex])
        self.zero_deg_in = list(omega.intersection(set(zero_deg_in)))
        self.zero_deg_in = list(omega.intersection(set(zero_deg_out)))

    def cut_edges(self):
        omega = [i.index for i in self.vertex]

        for vertex in self.vertex:
            keys_to_remove = []
            for succ in vertex.successors:
                if succ not in omega:
                    keys_to_remove.append(succ)
            for key in keys_to_remove:
                vertex.successors.pop(key)

            keys_to_remove.clear()
            for pred in vertex.predecessors:
                if pred not in omega:
                    keys_to_remove.append(pred)
            for key in keys_to_remove:
                vertex.predecessors.pop(key)


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex = vertices
        self.strong_connected_components: list[list[int]] = []
        self.lists_to_analize = [Subgraph(self.vertex)]
        self.zero_deg_in: list[int] = []
        self.zero_deg_out: list[int] = []

    class Direction(Enum):
        IN = "successors"
        OUT = "predecessors"

    def bfs_to_set(self, vertex_ind: int, direction: Direction) -> set[int]:
        reach = set()
        queue = [vertex_ind]
        while len(queue) > 0:
            current_vert_ind = queue.pop(0)
            current_vert = self.vertex[current_vert_ind]
            for vert_id in getattr(current_vert, direction.value):
                if vert_id not in reach:
                    queue.append(vert_id)
                    reach.add(vert_id)
        return reach

    def delete_vertex(self, vertex_ind: int):
        vertex = self.vertex[vertex_ind]
        for vert in vertex.successors.values():
            vert.predecessors.pop(vertex.index)
            if len(vert.predecessors) == 0:
                self.zero_deg_in.append(vert.index)
        for vert in vertex.predecessors.values():
            vert.successors.pop(vertex.index)
            if len(vert.successors) == 0:
                self.zero_deg_out.append(vert.index)

        vertex.predecessors.clear()
        vertex.successors.clear()

    def __str__(self):
        scc_info = "\n".join(
            str(component) for component in self.strong_connected_components
        )
        separator = "-----------------------------------------------\n\n"
        lists_to_analize_indices = []
        for subgraph in self.lists_to_analize:
            lists_to_analize_indices.append(
                [vertex.index for vertex in subgraph.vertex]
            )

        return f"Strongly Connected Components:\n{scc_info}\nLists to Analyze:\n{lists_to_analize_indices}\n{separator}"

    def leifman(self):
        while len(self.lists_to_analize) > 0:
            current_list = self.lists_to_analize.pop()
            current_list.init_zero_deg(self.zero_deg_in, self.zero_deg_out)
            current_list.cut_edges()
            current_list.reset_reachability_matrix()

            # 1 repeat as long as there are single vertices
            while (
                len(current_list.zero_deg_in) > 0 or len(current_list.zero_deg_out) > 0
            ):
                new_component = None
                if len(current_list.zero_deg_in) > 0:
                    new_component = current_list.zero_deg_in.pop()
                else:
                    new_component = current_list.zero_deg_out.pop()
                self.strong_connected_components.append([new_component])
                self.delete_vertex(new_component)
                current_list.vertex.remove(self.vertex[new_component])

            # 2 fill reachability matrix
            omega = set([i.index for i in current_list.vertex])
            start_node = current_list.vertex[0]
            in_span = self.bfs_to_set(start_node.index, self.Direction.IN)
            out_span = self.bfs_to_set(start_node.index, self.Direction.OUT)
            current_list.reachability_matrix[1][1] = list(
                in_span.intersection(out_span)
            )
            current_list.reachability_matrix[1][0] = list(in_span.difference(out_span))
            current_list.reachability_matrix[0][1] = list(out_span.difference(in_span))
            current_list.reachability_matrix[0][0] = list(
                omega.difference(in_span.union(out_span))
            )
            if len(current_list.reachability_matrix[1][1]) > 0:
                self.strong_connected_components.append(
                    current_list.reachability_matrix[1][1]
                )
            else:
                self.strong_connected_components.append([start_node.index])
                current_list.reachability_matrix[0][0].remove(start_node.index)
                self.delete_vertex(start_node.index)

            # 3 update list to analize
            for i, j in [(0, 1), (1, 0), (0, 0)]:
                if len(current_list.reachability_matrix[i][j]) > 0:
                    self.lists_to_analize.append(
                        Subgraph(
                            [
                                self.vertex[i]
                                for i in current_list.reachability_matrix[i][j]
                            ]
                        )
                    )
            print(f"current_list: {current_list}{self}\n ")

        for i in range(len(self.strong_connected_components)):
            self.strong_connected_components[i].sort()
            for j in range(len(self.strong_connected_components[i])):
                self.strong_connected_components[i][j] += 1

        self.strong_connected_components.sort()
        pprint(self.strong_connected_components)


with open("leifman.txt", "r") as file:

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

vertices = Vertices([Vertex({}, {}, i) for i in range(len(graph))])
for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i][j] == 1:
            vertices.vertex[i].successors[j] = vertices.vertex[j]
            vertices.vertex[j].predecessors[i] = vertices.vertex[i]

vertices.leifman()
