from math import inf
from pprint import pprint


def plus_one(arr):
    return [[x + 1 for x in row] for row in arr]


t = 0
with open("MatrixPaths.txt", "r") as file:

    graph: list[list[int]] = []
    predecessor: list[list[int]] = []
    for ind_x, line in enumerate(file):
        items = line.split()
        row = []
        row_pred = []
        for ind_y, item in enumerate(items):
            if item == "-":
                if ind_x == ind_y:
                    row.append(0)
                    row_pred.append(ind_x)
                else:
                    row.append(inf)
                    row_pred.append(-1)
            else:
                row.append(int(item))
                row_pred.append(ind_x)
        graph.append(row)
        predecessor.append(row_pred)

print(f"W{t}")
pprint(graph)

print(f"\nP{t}")
pprint(plus_one(predecessor))


def floyd_warshall() -> bool:
    global t
    err = False
    for _ in range(len(graph) - 1):
        for ind_x in range(len(graph)):
            for ind_y in range(len(graph)):
                if ind_x == t and ind_y == t:
                    continue
                if graph[ind_x][ind_y] > graph[ind_x][t] + graph[t][ind_y]:
                    graph[ind_x][ind_y] = graph[ind_x][t] + graph[t][ind_y]
                    predecessor[ind_x][ind_y] = predecessor[t][ind_y]
                if ind_x == ind_y and graph[ind_x][ind_y] < 0:
                    err = True
        t += 1
        print(f"W{t}")
        pprint(graph)

        print(f"\nP{t}")
        pprint(plus_one(predecessor))
        print("____________________________")
        if err:
            return err
    return err


err = floyd_warshall()
if err:
    print("Ujemny cykl. Nie ma rozwiazania.")
else:
    print("Poprawnie")
