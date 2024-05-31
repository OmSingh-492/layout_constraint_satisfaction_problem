from pyomo.environ import *
import matplotlib.pyplot as plt

def solver(M):
    def non_linear_constraint(model, i, j):
        if i >= j:
            return Constraint.Skip
        x1 = 0 if i in gamma else model.x[i]
        x2 = 0 if j in gamma else model.x[j]
        distance = (x1 - x2) ** 2 + (model.y[i] - model.y[j]) ** 2
        radial = (r_created[i] + r_created[j]) ** 2
        if (i, j) in adjacency:
            return (lower * radial, distance, upper * radial)
        return distance >= lower * radial

    def plot(optimal_x, optimal_y, entries, mapping, lower, upper):
        fig, ax = plt.subplots()
        for i in range(n):
            rect_created = plt.Rectangle((optimal_x[i], optimal_y[i]), entries[i][0], entries[i][1], fill=False, color="blue")
            ax.add_patch(rect_created)
            plt.text(optimal_x[i] + 0.2, optimal_y[i] + 0.2, mapping[i], fontsize=4, ha="center", va="center", color="black")     
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Final Plot")
        plt.axis("equal")
        plt.savefig("output.png")

    def generate_inputs():
        sizes, indices, mapping = {}, {}, {}
        adjacency, gamma, anchors = set(), set(), set()
        with open("sizes.txt", "r") as file:
            for line in file:
                str_value, length_value, breadth_value = line.strip().split(",")
                sizes[str_value] = (float(length_value), float(breadth_value))
        entries = [0 for x in range(len(sizes))]
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

    n, entries, gamma, adjacency, mapping = generate_inputs()
    model = ConcreteModel()
    model.Nodes = Set(initialize=range(n))
    model.NonAnchors = Set(initialize=set(range(n)) - gamma)

    model.x = Var(model.NonAnchors, bounds=NonNegativeReals)
    model.y = Var(model.Nodes, within=NonNegativeReals)
    
    model.non_linear_constraints = Constraint(model.Nodes, model.Nodes, rule=lambda model, i, j: non_linear_constraint(model, i, j, lower=lower, upper=upper))
    
    solver = SolverFactory("ipopt", options={"max_iter": 40000})
    solver.solve(model, tee=True)

    optimal_x = [value(model.x[i]) for i in model.NonAnchors] + [0 for _ in range(len(gamma))]
    optimal_y = [value(model.y[i]) for i in model.Nodes]

    print(optimal_x, optimal_y)
    plot(optimal_x, optimal_y, entries, mapping, lower, upper)
    
if __name__ == "__main__":
    solver(M)
    
"""

M = 100  # Adjust M as needed

# Introduce binary variables to represent each OR condition:
model.z1 = Var(domain=Binary)
model.z2 = Var(domain=Binary)
model.z3 = Var(domain=Binary)
model.z4 = Var(domain=Binary)

# Enforce one of the conditions must hold:
model.Add(model.z1 + model.z2 + model.z3 + model.z4 >= 1)

# Link binary variables to original constraints using Big-M:
x[idx1] + entries[idx1][0] - x[idx2] <= 0
OR
x[idx2] + entries[idx2][0] - x[idx1] <= 0

model.Add(x[idx1] + entries[idx1][0] - x[idx2] <= M * (1 - model.z1))  # Enforce x[idx1] + entries[idx1][0] == x[idx2] if z1 = 1
model.Add(x[idx2] + entries[idx2][0] - x[idx1] <= M * (1 - model.z2))  # Enforce x[idx2] + entries[idx2][0] == x[idx1] if z2 = 1
model.Add(y[idx1] + entries[idx1][1] - y[idx2] <= M * (1 - model.z3))  # Enforce y[idx1] + entries[idx1][1] == y[idx2] if z3 = 1
model.Add(y[idx2] + entries[idx2][1] - y[idx1] <= M * (1 - model.z4))  # Enforce y[idx2] + entries[idx2][1] == y[idx1] if z4 = 1
"""