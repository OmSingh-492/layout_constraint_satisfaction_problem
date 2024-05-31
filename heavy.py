from pyomo.environ import *
import matplotlib.pyplot as plt

def solver(lower, upper, multiplier):
    def non_linear_constraint(model, i, j, lower, upper):
        if i >= j:
            return Constraint.Skip
        x1 = 0 if i in gamma else model.x[i]
        x2 = 0 if j in gamma else model.x[j]
        distance = (x1 - x2) ** 2 + (model.y[i] - model.y[j]) ** 2
        radial = (r_created[i] + r_created[j]) ** 2
        if (i, j) in adjacency:
            return (lower * radial, distance, upper * radial)
        return distance >= lower * radial

    def plot(optimal_x, optimal_y, r_original, r_created, mapping, lower, upper, multiplier):
        fig, ax = plt.subplots()
        for i in range(n):
            circle_created = plt.Circle((optimal_x[i], optimal_y[i]), r_created[i], fill=False, color="blue")
            ax.add_patch(circle_created)
            circle_original = plt.Circle((optimal_x[i], optimal_y[i]), r_original[i], fill=False, color="red")
            ax.add_patch(circle_original)
            plt.text(optimal_x[i] + 0.2, optimal_y[i] + 0.2, mapping[i], fontsize=4, ha="center", va="center", color="black")

        min_x, min_y, max_x, max_y = optimal_x[0] - r_created[0], optimal_y[0] - r_created[0], optimal_x[0] + r_created[0], optimal_y[0] + r_created[0]
        for index in range(n):
            min_x = min(min_x, optimal_x[index] - r_created[index])
            max_x = max(max_x, optimal_x[index] + r_created[index])
            min_y = min(min_y, optimal_y[index] - r_created[index])
            max_y = max(max_y, optimal_y[index] + r_created[index])

        rect = plt.Rectangle((min_x, min_y), max_x - min_x, max_y - min_y, fill=False, color="red", linestyle="--", linewidth=2)
        ax.add_patch(rect)
        plt.xlabel("X-axis")
        plt.ylabel("Y-axis")
        plt.title("Final Plot with Bounding Box")
        plt.axis("equal")
        path = "outputs/" + str(lower) + "_" + str(upper) + "_" + str(multiplier) + ".png"
        plt.show()

    def generate_inputs(multiplier):
        sizes, indices, mapping = {}, {}, {}
        adjacency, gamma, anchors = set(), set(), set()
        with open("sizes.txt", "r") as file:
            for line in file:
                str_value, size_value = line.strip().split(",")
                sizes[str_value] = float(size_value)
        r_original = [0 for x in range(len(sizes))]
        r_created = [0 for x in range(len(sizes))]
        index = len(sizes) - 1
        with open("anchors.txt", "r") as file:
            for line in file:
                current = line.strip()
                print(current)
                indices[current] = index
                anchors.add(current)
                mapping[index] = current
                r_original[index] = sizes[current]
                r_created[index] = r_original[index] * multiplier
                index -= 1
        index = 0
        for key in sizes:
            if key not in anchors:
                indices[key] = index
                mapping[index] = key
                r_original[index] = sizes[key]
                r_created[index] = r_original[index] * multiplier
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
        return len(sizes), r_original, r_created, gamma, adjacency, mapping

    n, r_original, r_created, gamma, adjacency, mapping = generate_inputs(multiplier)
    print(n, r_original, r_created, gamma, adjacency, mapping)
    model = ConcreteModel()

    model.Nodes = Set(initialize=range(n))
    model.NonAnchors = Set(initialize=set(range(n)) - gamma)

    bounds = []
    for index in range(n - len(gamma)):
        bounds.append((r_created[index], None))

    model.x = Var(model.NonAnchors, bounds=bounds)
    model.y = Var(model.Nodes, within=NonNegativeReals)
    
    model.non_linear_constraints = Constraint(model.Nodes, model.Nodes, rule=lambda model, i, j: non_linear_constraint(model, i, j, lower=lower, upper=upper))
    
    solver = SolverFactory("ipopt", options={"max_iter": 40000})
    solver.solve(model, tee=True)

    optimal_x = [value(model.x[i]) for i in model.NonAnchors] + [0 for _ in range(len(gamma))]
    optimal_y = [value(model.y[i]) for i in model.Nodes]

    print(optimal_x)
    print(optimal_y)
    plot(optimal_x, optimal_y, r_original, r_created, mapping, lower, upper, multiplier)
    
if __name__ == "__main__":
    solver(0.8, 1.2, 1.1)
    """
    lower_list = [0.40, 0.50, 0.60, 0.70, 0.80, 0.90, 1.00]
    upper_list = [1.00, 1.10, 1.20, 1.30, 1.40, 1.50, 1.60, 1.70, 1.80]
    mult = [1.0, 1.05, 1.10, 1.15, 1.20, 1.25, 1.30]
    for lower in lower_list:
        for upper in upper_list:
            for multiplier in mult:
                solver(lower, upper, multiplier)
    """