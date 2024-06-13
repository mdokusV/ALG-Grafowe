from pprint import pprint
from dataclasses import dataclass, field
from queue import Queue
import sys
from typing import Dict
from enum import Enum

from numpy import sign

INF = sys.maxsize


class Direction(Enum):
    FORWARD = "forward"
    BACKWARD = "backward"


@dataclass
class Edge:
    capacity: int
    start: "Vertex"
    end: "Vertex"
    flow: int = 0


@dataclass
class Vertex:
    index: int
    successors: Dict["Vertex", Edge] = field(default_factory=dict)
    predecessors: Dict["Vertex", Edge] = field(default_factory=dict)
    change: int = 0
    path_edge_predecessor: "Edge|None" = None
    checked: bool = False

    def __hash__(self) -> int:
        return self.index

    def __eq__(self, other) -> bool:
        return self.index == other.index

    def reset(self):
        self.change = 0
        self.checked = False
        self.path_edge_predecessor = None

    def __str__(self) -> str:

        successors_str = ", ".join(
            [f"{key.index}:{value.capacity}" for key, value in self.successors.items()]
        )
        predecessors_str = ", ".join(
            [
                f"{key.index}:{value.capacity}"
                for key, value in self.predecessors.items()
            ]
        )

        return f"[{self.index}]\t successors: {successors_str:<20}  predecessors: {predecessors_str:<20}"


def find_best_flow():
    while True:
        found_new_path, minimal_cut = find_increasing_path(vertices[0])
        if not found_new_path:
            print_end(minimal_cut)
            break

        update_edges()

        reset_vertices()


def update_edges():
    vertex = vertices[-1]
    increasing_path = [vertex]
    flow_change = vertex.change
    while vertex.path_edge_predecessor is not None:
        edge = vertex.path_edge_predecessor
        edge.flow += sign(vertex.change) * flow_change
        if vertex.change > 0:
            vertex = vertex.path_edge_predecessor.start
        else:
            vertex = vertex.path_edge_predecessor.end
        increasing_path.append(vertex)

    print("Ścieżka powiększająca:", end="\t")
    print(", ".join(str(vertex.index + 1) for vertex in increasing_path[::-1]))
    print("Dodana wartość przepływu:", vertices[-1].change)
    print(
        "Aktualny przepływ:", sum(edge.flow for edge in vertices[0].successors.values())
    )
    print()


def reset_vertices():
    for vertex in vertices:
        vertex.reset()


def print_end(minimal_cut: set[Vertex]):
    print("Cięcie minimalne:", end="\t")
    print(", ".join(str(vertex.index + 1) for vertex in minimal_cut))

    print("Wartości przepływu:")
    for edge in edges:
        print(f"({edge.start.index + 1}, {edge.end.index + 1}): {edge.flow}")

    print(
        "Maksymalny przepływ:",
        sum(edge.flow for edge in vertices[0].successors.values()),
    )


def find_increasing_path(start_vertex: Vertex) -> tuple[bool, set[Vertex]]:
    def check_vertex(direction: Direction):
        # check if visited and checked
        if direction == Direction.FORWARD:
            next_vertex = edge.end
        else:
            next_vertex = edge.start
        if next_vertex.checked is True:
            return

        # check flow
        if direction == Direction.FORWARD:
            available_flow = min(edge.capacity - edge.flow, abs(checking_vertex.change))
        else:
            available_flow = -min(edge.flow, abs(checking_vertex.change))

        if available_flow == 0:
            return
        if next_vertex.change != 0:
            if abs(available_flow) <= abs(next_vertex.change):
                return

        next_vertex.change = available_flow
        next_vertex.path_edge_predecessor = edge
        queue.put(next_vertex)
        minimal_cut.add(next_vertex)

    # init
    minimal_cut: set[Vertex] = set()
    queue: Queue[Vertex] = Queue()
    start_vertex.change = INF
    queue.put(start_vertex)
    minimal_cut.add(start_vertex)

    while not queue.empty():
        checking_vertex = queue.get()
        checking_vertex.checked = True

        if checking_vertex == vertices[-1]:
            return True, minimal_cut

        # check all successors
        for edge in checking_vertex.successors.values():
            check_vertex(Direction.FORWARD)

        # check all predecessors
        for edge in checking_vertex.predecessors.values():
            check_vertex(Direction.BACKWARD)

    return False, minimal_cut


with open("graph13.txt", "r") as file:

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


vertices = [Vertex(i) for i in range(len(graph))]
edges: list[Edge] = []
for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i][j] > 0:
            new_edge = Edge(graph[i][j], vertices[i], vertices[j])
            edges.append(new_edge)
            vertices[i].successors[vertices[j]] = new_edge
            vertices[j].predecessors[vertices[i]] = new_edge

for vertex in vertices:
    print(vertex)

find_best_flow()
