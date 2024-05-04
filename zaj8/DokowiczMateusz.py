from pprint import pprint


COMPLETE_GRAPH = True


class CashingItems:

    def __init__(self, all_subtrees: list = [], tree_number: int = 0):
        self.all_subtrees: list[list[Edge]] = all_subtrees
        self.new_subtrees: list[list[Edge]] = all_subtrees
        self.tree_number: int = tree_number

    def add(self, new_edges: list[Edge], new_tree_number: int):
        self.tree_number += new_tree_number

        for subtree in self.new_subtrees:
            subtree += new_edges

        if len(self.new_subtrees) != self.tree_number:
            raise SystemError("Number Of trees does not match")


class TreeCache:

    def __init__(
        self, roots: list | set, children: list | set, cashing_items: CashingItems
    ):
        self.roots: frozenset = frozenset(roots)
        self.disconnected: frozenset = frozenset(children)
        self.all_subtrees: list[list[Edge]] = cashing_items.all_subtrees
        self.tree_number: int = cashing_items.tree_number

    def __hash__(self) -> int:
        return hash((self.roots, self.disconnected))

    def __eq__(self, other) -> bool:
        return self.disconnected == other.disconnected and self.roots == other.roots

    def __str__(self) -> str:
        return f"roots: {self.roots}, disconnected: {self.disconnected}"


class Vertex:
    def __init__(self, index: int):
        self.index = index
        self.connects: list[Vertex] = []
        self.free_children: dict[int, Vertex] = {}
        self.currently_permuting_children: list[Vertex] = []
        self.parent: Vertex | None = None
        self.marked: bool = False
        self.degree = 0

    def __str__(self):
        return f"[{self.index}] degree: {self.degree}, connects:{[vert.index for vert in self.connects]}"

    def remove_child(self) -> bool:
        orphan = False
        for vert in self.connects:
            if self.index in vert.free_children:
                vert.free_children.pop(self.index)
                if len(vert.free_children) == 0 and not self.marked:
                    orphan = True
        return orphan

    def add_child(self):
        for vert in self.connects:
            vert.free_children[self.index] = self


class Edge:
    def __init__(self, v1: Vertex, v2: Vertex):
        self.v1 = v1.index
        self.v2 = v2.index


def get_permutation(items: list[Vertex], n: int) -> tuple[list[Vertex], bool]:
    if len(items) == 0:
        if n == 0:
            return [], False
        else:
            return [], True
    binary_list = [not (bool(int(i))) for i in list(bin(n)[2:].zfill(len(items)))]
    if len(binary_list) != len(items):
        return [], True
    return [items[i] for i, v in enumerate(binary_list) if v == True], False


def show_permutation(items: list[Vertex]) -> str:
    out_string = " ".join([str(item.index) for item in items])
    # print(out_string)
    return out_string


class Vertices:
    def __init__(self, vertices: list[Vertex]):
        self.vertex_list = vertices
        self.tree_cache: dict[TreeCache, TreeCache] = {}
        self.unmarked_vertices: set[Vertex] = set(self.vertex_list)
        self.waiting_to_check: list[Vertex] = []
        self.number_of_trees = 0
        self.trees: list[tuple[Vertex, Vertex]] = []

    def __str__(self):
        return "".join([str(vertex) + "\n" for vertex in self.vertex_list])

    def init_dfs(self, vertex: Vertex):
        vertex.remove_child()
        self.unmarked_vertices.remove(vertex)
        self.dfs(vertex)
        print(self.number_of_trees)

    def get_tree_cache(self, cashing_items) -> CashingItems | None:
        roots = []
        if len(self.waiting_to_check) >= 1:
            roots = self.waiting_to_check

        checking_tree = TreeCache(roots, self.unmarked_vertices, cashing_items)
        if checking_tree in self.tree_cache:
            return CashingItems(
                self.tree_cache[checking_tree].all_subtrees,
                self.tree_cache[checking_tree].tree_number,
            )

        return None

    def add_to_cache(self, cashing_items: CashingItems):
        new_tree = TreeCache(
            self.waiting_to_check, self.unmarked_vertices, cashing_items
        )
        self.tree_cache[new_tree] = new_tree

    def dfs(self, vertex: Vertex) -> CashingItems:
        # print(vertex)

        # initiate permutation for all available children
        cashing_items = CashingItems()
        permutation_number = 0
        vertex.currently_permuting_children = list(vertex.free_children.values())
        permutation, err = get_permutation(
            vertex.currently_permuting_children, permutation_number
        )

        # go threw all permutations
        if err == True:
            raise SystemError("Internal system error in dfs")
        while True:
            if not self.add_children_from_permutation(permutation, vertex):
                found_cashed_tree = self.get_tree_cache(cashing_items)
                if found_cashed_tree is not None:
                    self.number_of_trees += found_cashed_tree.tree_number
                    cashing_items.add(found_cashed_tree)
                else:
                    # when there is no more waiting vertices we backtrack and add tree if there is one
                    if len(self.waiting_to_check) == 0:
                        if len(self.unmarked_vertices) == 0:
                            self.number_of_trees += 1
                            cashing_items.tree_number += 1
                            if vertex.parent is None:
                                raise SystemError("Parent is None")
                            cashing_items.all_subtrees.append(
                                [Edge(vertex, vertex.parent)]
                            )
                        self.waiting_to_check.append(vertex)
                        return cashing_items

                    # go deeper to next vertex
                    next_vertex = self.waiting_to_check.pop()
                    new_trees = self.dfs(next_vertex)
                    cashing_items.add(new_trees)
                    self.add_to_cache(new_trees)

            # backtrack to previous vertex state as if we have not visited its children
            # print(f"back from {next_vertex.index} to {vertex.index}")
            self.reverse_add_children_from_permutation(permutation)

            # generate next permutation
            permutation_number += 1
            permutation, overflow = get_permutation(
                vertex.currently_permuting_children, permutation_number
            )

            # we checked all permutations so we return
            if overflow:
                self.waiting_to_check.append(vertex)
                return cashing_items

    def add_children_from_permutation(
        self, permutation: list[Vertex], parent: Vertex
    ) -> bool:
        is_orphan = False
        for child in permutation:
            if child in self.unmarked_vertices:
                self.waiting_to_check.append(child)
                self.unmarked_vertices.remove(child)
                child.marked = True
                child.parent = parent
                orphan = child.remove_child()
                if orphan:
                    is_orphan = True
        return is_orphan

    def reverse_add_children_from_permutation(self, permutation: list[Vertex]):
        for child in permutation:
            self.waiting_to_check.pop()
            self.unmarked_vertices.add(child)
            child.marked = False
            child.parent = None
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
# pprint(graph)

if COMPLETE_GRAPH:
    size = 5
    graph = [[1 if i != j else 0 for j in range(size)] for i in range(size)]


vertices = Vertices([Vertex(i) for i in range(len(graph))])
for i in range(len(graph)):
    for j in range(len(graph)):
        if graph[i][j] == 1:
            vertices.vertex_list[i].connects.append(vertices.vertex_list[j])
            vertices.vertex_list[i].degree += 1
            vertices.vertex_list[i].free_children[j] = vertices.vertex_list[j]

# print(vertices)

# DFS


initial_root = vertices.vertex_list[0]
vertices.init_dfs(initial_root)

if COMPLETE_GRAPH:
    print("expected: ", pow(size, size - 2))
    print("Is equal:", vertices.number_of_trees == pow(size, size - 2))
