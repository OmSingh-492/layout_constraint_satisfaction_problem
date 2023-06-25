import sys
from shapely.geometry import Polygon, box
from shapely.affinity import translate
from shapely.ops import unary_union
import matplotlib.pyplot as plt

def populate(adj_list, sides, anchors):
    # FILL IN WITH METHOD TO POPULATE THE DATA STRUCTURES. KEEP INTEGRAL SIDE LENGTHS.
    adj_list = {"B0": [10], "B1": [10], "B2": [10], "B3": [10, 10, 10, 10],
               "B4": [10, 10], "B5": [10], "B6": [10, 10, 10, 15], "B7": [10],
               "B8": [10], "B9": [10, 10]}
    sides = [15, 10, 20, 80, 15, 12, 25, 15, 20, 20]
    anchors = [0, 3, 4, 6, 9]
    return adj_list, sides, anchors

def create_envelopes(adj_list, sides):
    # Create an envelope for master-slaves, to pack the envelopes later instead of actual squares.
    for rect in adj_list.keys():
        slaves = adj_list[rect]
        side_master = sides[int(rect[1])]
        number_slaves = len(slaves)
        """
        Refer notes to visualise what all edge cases have been excluded, and the reasoning behind the choices.
        Assumption: Number of slaves <= 4.
        """
        if number_slaves == 1:
            side = slaves[0] + side_master
        elif number_slaves == 2:
            side = slaves[0] + slaves[1] + side_master
        elif number_slaves == 3:
            side = slaves[2] + max(slaves[0], slaves[1]) + side_master
        else:
            side = max(slaves[2], slaves[3]) + max(slaves[0], slaves[1]) + side_master
        sides[int(rect[1])] = side
    # First function which should be ran for creating envelopes.
    return adj_list, sides

def translate_bottom(last, existing, side):
    # Idea: Place the initial polygon at the bottom left, and translate it till it reaches bottom right.
    coordinates = list(last.exterior.coords)
    coordinates[3] = coordinates[0]
    coordinates[0] = tuple(x - y for x, y in zip(coordinates[3], (0, side)))
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side, 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side)))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area = sys.maxsize
    possible = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[0] < last.bounds[2]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible:
                possible = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_bottom = translated
                min_area = ar
        translated = translate(translated, xoff=1.0)
    if not possible:
        return last, -1
    return optimum_bottom, min_area

def translate_top(last, existing, side):
    # Idea: Place the initial polygon at the top left, and translate it till it reaches top right.
    coordinates = list(last.exterior.coords)
    coordinates[0] = coordinates[3]
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side, 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side)))
    coordinates[3] = tuple(x - y for x, y in zip(coordinates[2], (side, 0)))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area = sys.maxsize
    possible = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[0] < last.bounds[2]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible:
                possible = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_top = translated
                min_area = ar
        translated = translate(translated, xoff=1.0)
    if not possible:
        return last, -1
    return optimum_top, min_area

def translate_top_right(last, existing, side):
    # Idea: Place the initial polygon on the right, and in case of equal areas, eveolve towards the top.
    coordinates = list(last.exterior.coords)
    coordinates[0] = coordinates[1]
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side, 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side)))
    coordinates[3] = tuple(x + y for x, y in zip(coordinates[0], (0, side)))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area = sys.maxsize
    possible = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[1] < last.bounds[3]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible:
                possible = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_rt = translated
                min_area = ar
        translated = translate(translated, yoff=1.0)
    if not possible:
        return last, -1
    return optimum_rt, min_area

def translate_top_left(last, existing, side):
    # Idea: Place the initial polygon on the right, and in case of equal areas, eveolve towards the bottom.
    coordinates = list(last.exterior.coords)
    coordinates[3] = coordinates[2]
    coordinates[0] = tuple(x - y for x, y in zip(coordinates[3], (0, side)))
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side, 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side)))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area = sys.maxsize
    possible = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[3] > last.bounds[1]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible:
                possible = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_rb = translated
                min_area = ar
        translated = translate(translated, yoff=-1.0)
    if not possible:
        return last, -1
    return optimum_rb, min_area

def plot(to_plot, index):
    # A generic plotting function.
    x, y = to_plot.exterior.xy
    plt.plot(x, y)
    x_centroid, y_centroid = to_plot.centroid.coords[0]
    plt.annotate(index, (x_centroid, y_centroid), color="red", ha="center", va="center", fontsize=8)

def layout(anchors, sides):
    # Assumption: Between consecutive bins, there are atleast two squares.
    existing = Polygon([(0, 0), (sides[0], 0), (sides[0], sides[0]), (0, sides[0]), (0, 0)])
    last = existing
    # Plot the polygon
    plot(last, 0)
    left_index = 0
    for right_index in anchors[1::]:
        mid = (right_index + left_index) // 2
        for index in range(left_index + 1, mid + 1):
            side = sides[index]
            optimum_top, min_top = translate_top(last, existing, side)
            optimum_rt, min_rt = translate_top_right(last, existing, side)
            if min_top >= min_rt and min_rt != -1:
                existing = unary_union([existing, optimum_rt])
                last = optimum_rt
            elif min_rt == -1 and min_top == -1:
                optimum_bottom, min_bot = translate_bottom(last, existing, side)
                optimum_rb, min_rb = translate_top_left(last, existing, side)
                if min_bot <= min_rb and min_bot != -1:
                    existing = unary_union([existing, optimum_bottom])
                    last = optimum_bottom
                else:
                    existing = unary_union([existing, optimum_rb])
                    last = optimum_rb
            else:
                existing = unary_union([existing, optimum_top])
                last = optimum_top
            # Plot the polygon
            plot(last, index)
        for index in range(mid + 1, right_index):
            side = sides[index]
            optimum_bottom, min_bot = translate_bottom(last, existing, side)
            optimum_rb, min_rb = translate_top_left(last, existing, side)
            if min_bot <= min_rb and min_bot != -1:
                existing = unary_union([existing, optimum_bottom])
                last = optimum_bottom
            elif min_bot == -1 and min_rb == -1:
                optimum_top, min_top = translate_top(last, existing, side)
                optimum_rt, min_rt = translate_top_right(last, existing, side)
                if min_top >= min_rt and min_rt != -1:
                    existing = unary_union([existing, optimum_rt])
                    last = optimum_rt
                else:
                    existing = unary_union([existing, optimum_top])
                    last = optimum_top
            else:
                existing = unary_union([existing, optimum_rb])
                last = optimum_rb
            # Plot the polygon
            plot(last, index)
        # Place the envelope separately on the x-axis. Use red colour for its borders.
        x_min = last.bounds[0]
        x_max = last.bounds[2]
        side = sides[right_index]
        translated = Polygon([(x_min, 0), (x_min + side, 0), (x_min + side, side), (x_min, side), (x_min, 0)])
        min_area = sys.maxsize
        if existing.touches(translated) or existing.disjoint(translated):
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_env = translated
                min_area = ar
        else:
            optimum_env = translate(translated, xoff=x_max - translated.bounds[0])
        existing = unary_union([existing, optimum_env])
        last = optimum_env
        left_index = right_index
        # Plot the polygon.
        plot(last, right_index)

def main():
    """
    Both slaves and masters have been taken to be squares.
    Number the bins so that Bi is close to ith envelope.
    Ex: adj_list = {"B7": [2, 4, 2, 4], ...}
    sides = [10, 15, 1, 4, ...]
    anchors = [1, 7, 9, ...]
    To get the length of B7 master, look at the 7th index in the sides list.
    Keep everything zero-indexed.
    adj_list = {} # A dictionary, where marked nodes are mapped to their alphabetical slaves' sides' list
    sides = [] # A list of side lengths. For masters whose envelopes haven't been created, length = length of master.
    anchors = [] # A list of anchors, i.e. squares constrained on the x-axis.
    """
    adj_list, sides, anchors = populate({}, [], [])
    adj_list, sides = create_envelopes(adj_list, sides)
    plt.tight_layout()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    print(sides)
    layout(anchors, sides)
    plt.show()

if __name__ == "__main__":
    main()
