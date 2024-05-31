from ortools.sat.python import cp_model
import sys
import math

def generate_inputs():
        sizes, indices, mapping = {}, {}, {}
        adjacency, gamma, anchors = set(), set(), set()
        with open("sizes.txt", "r") as file:
            for line in file:
                str_value, length_value, breadth_value = line.strip().split(",")
                sizes[str_value] = (float(length_value), float(breadth_value))
        entries = [(0, 0) for y in range(len(sizes))]
        index = len(sizes) - 1
        with open("anchors.txt", "r") as file:
            for line in file:
                current = line.strip()
                indices[current] = index
                anchors.add(current)
                mapping[index] = current
                entries[index] = sizes[current]
                index -= 1
        index = 0
        for key in sizes:
            if key not in anchors:
                indices[key] = index
                mapping[index] = key
                entries[index] = sizes[key]
                index += 1
        with open("edges.txt", "r") as file:
            for line in file:
                key1, key2 = line.strip().split(",")
                index1, index2 = indices[key1], indices[key2]
                if index1 > index2:
                    index1, index2 = index2, index1
                adjacency.add((index1, index2))
        with open("anchors.txt", "r") as file:
            for line in file:
                gamma.add(indices[line.strip()])
        return len(sizes), entries, gamma, adjacency, mapping

if __name__ == "__main__":
    model = cp_model.CpModel()
    n, entries, gamma, adjacency, mapping = generate_inputs()
    x = [model.NewIntVar(0, sys.maxsize, f"x_{index}") for index in range(n)]
    y = [model.NewIntVar(0, sys.maxsize, f"y_{index}") for index in range(n)]
    for index in gamma:
        model.Add(y[index] == 0)
    for idx1 in range(n):
        for idx2 in range(idx1 + 1, n):
            if (idx1, idx2) in adjacency:
                model.Add(x[idx1] + entries[idx1][0] == x[idx2] or x[idx2] + entries[idx2][0] == x[idx1] or y[idx1] + entries[idx1][1] == y[idx2] or y[idx2] + entries[idx2][1] == y[idx1])
            else:
                model.Add(x[idx1] + entries[idx1][0] <= x[idx2] or x[idx2] + entries[idx2][0] <= x[idx1])
                model.Add(y[idx1] + entries[idx1][1] <= y[idx2] or y[idx2] + entries[idx2][1] <= y[idx1])
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    res_x, res_y = [], []
    if status == cp_model.FEASIBLE:
        print("Solution found:")
        for index in range(n):
            res_x.append(solver.Value(x[index]))
            res_y.append(solver.Value(y[index]))
    else:
        print("No solution found.")
    print(res_x, res_y)