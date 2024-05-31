from pyomo.environ import *
import matplotlib.pyplot as plt

def non_linear_constraint(model, i, j):
    if i >= j:
        return Constraint.Skip
    distance = abs(model.x[i] - model.x[j]) + abs(model.y[i] - model.y[j])
    if (i, j) in adjacency:
        return distance - (model.r[i] + model.r[j]) == 0
    return (model.r[i] + model.r[j]) - distance <= 0

def fixed_constraint(model, index):
    return model.y[index] == 0

def plot(optimal_x, optimal_y, r, mapping):
    fig, ax = plt.subplots()
    for i in range(n):
        circle = plt.Circle((optimal_x[i], optimal_y[i]), r[i], fill=False, color="blue")
        ax.add_patch(circle)
        plt.text(optimal_x[i] + 0.2, optimal_y[i] + 0.2, mapping[i], fontsize=7, ha="center", va="center", color="black")

    min_x, min_y, max_x, max_y = optimal_x[0] - r[0], optimal_y[0] - r[0], optimal_x[0] + r[0], optimal_y[0] + r[0]
    for index in range(n):
        min_x = min(min_x, optimal_x[index] - r[index])
        max_x = max(max_x, optimal_x[index] + r[index])
        min_y = min(min_y, optimal_y[index] - r[index])
        max_y = max(max_y, optimal_y[index] + r[index])

    rect = plt.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, fill=False, color="red", linestyle="--", linewidth=2)
    ax.add_patch(rect)
    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Final Plot with Bounding Box")
    plt.axis("equal")
    plt.show()

def plot_intermediate(optimal_x, optimal_y, r, mapping):
    fig, ax = plt.subplots()
    for i in range(n):
        circle = plt.Circle((optimal_x[i], optimal_y[i]), r[i], fill=False, color="blue")
        ax.add_patch(circle)
        plt.text(optimal_x[i] + 0.2, optimal_y[i] + 0.2, mapping[i], fontsize=7, ha="center", va="center", color="black")

    plt.xlabel("X-axis")
    plt.ylabel("Y-axis")
    plt.title("Intermediate Plot")
    plt.axis("equal")
    plt.show()
    
def generate_inputs():
    sizes, indices, mapping = {}, {}, {}
    adjacency = set()
    r, gamma= [], []
    with open("sizes.txt", "r") as file:
        for line in file:
            str_value, size_value = line.strip().split(",")
            sizes[str_value] = float(size_value)
    index = 0
    for key in sizes:
        indices[key] = index
        mapping[index] = key
        r.append(sizes[key])
        index += 1
    n = index
    with open("edges.txt", "r") as file:
        for line in file:
            key1, key2 = line.strip().split(",")
            index1, index2 = indices[key1], indices[key2]
            if index1 > index2:
                index1, index2 = index2, index1
            adjacency.add((index1, index2))
    with open("anchors.txt", "r") as file:
        for line in file:
            gamma.append(indices[line.strip()])
    return n, r, gamma, adjacency, mapping

n, r, gamma, adjacency, mapping = generate_inputs()
model = ConcreteModel()

model.Nodes = Set(initialize=range(n))
model.Gamma = Set(initialize=gamma)

model.x = Var(model.Nodes, within=NonNegativeReals)
model.y = Var(model.Nodes, within=NonNegativeReals)
model.r = Param(model.Nodes, initialize=lambda model, i: r[i])

model.non_linear_constraints = Constraint(model.Nodes, model.Nodes, rule=non_linear_constraint)
model.fixed_constraints = Constraint(model.Gamma, rule=fixed_constraint)

solver = SolverFactory("ipopt", options={"max_iter": 30000})
solver.solve(model, tee=True)

optimal_x = [value(model.x[i]) for i in model.Nodes]
optimal_y = [value(model.y[i]) for i in model.Nodes]

plot(optimal_x, optimal_y, r, mapping)