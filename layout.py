import sys
from shapely.geometry import Polygon, box
from shapely.affinity import translate
from shapely.ops import unary_union
import matplotlib.pyplot as plt

def populate(adj_list, sides, anchors):
    # FILL IN WITH METHOD TO POPULATE THE DATA STRUCTURES. KEEP INTEGRAL SIDE LENGTHS.
    adj_list = {0: [[10, 5]], 1: [[10, 5]], 2: [[5, 10]], 3: [[10, 10], [10, 5], [10, 10], [5, 10]],
               4: [[10, 5], [5, 10]], 5: [[10, 10]], 6: [[10, 5], [5, 10], [5, 10]], 7: [[5, 10]],
               8: [[5, 10]], 9: [[10, 10], [10, 5]]}
    sides = [[15, 25], [10, 20], [20, 30], [80, 100], [15, 35], [12, 22], [25, 50], [15, 25], [20, 30], [20, 40]]
    anchors = [0, 3, 6, 9]
    return adj_list, sides, anchors

def translate_bottom(last, existing, side):
    # Idea: Place the initial polygon at the bottom left, and translate it till it reaches bottom right.
    
    # sides[0] representing length and sides[1] representing breadth.
    coordinates = list(last.exterior.coords)
    coordinates[3] = coordinates[0]
    coordinates[0] = tuple(x - y for x, y in zip(coordinates[3], (0, side[1])))
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[0], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[1])))
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
    
    # sides[0] representing breadth and sides[0] represnting length.
    coordinates = list(last.exterior.coords)
    coordinates[3] = coordinates[0]
    coordinates[0] = tuple(x - y for x, y in zip(coordinates[3], (0, side[0])))
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[1], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[0])))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area_rotated = sys.maxsize
    possible_rotated = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[0] < last.bounds[2]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible_rotated:
                possible_rotated = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_bottom_rotated = translated
                min_area_rotated = ar
        translated = translate(translated, xoff=1.0)
    
    # Returning the polygon associated with the minimum envelope area.
    if not possible and not possible_rotated:
        return last, -1
    elif not possible and possible_rotated:
        return optimum_bottom_rotated, min_area_rotated
    elif possible and not possible_rotated:
        return optimum_bottom, min_area
    else:
        if min_area <= min_area_rotated:
            return optimum_bottom, min_area
        else:
            return optimum_bottom_rotated, min_area_rotated

def translate_top(last, existing, side):
    # Idea: Place the initial polygon at the top left, and translate it till it reaches top right.
    
    # sides[0] representing length and sides[1] representing breadth.
    coordinates = list(last.exterior.coords)
    coordinates[0] = coordinates[3]
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[0], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[1])))
    coordinates[3] = tuple(x - y for x, y in zip(coordinates[2], (side[0], 0)))
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
    
    # sides[0] representing breadth and sides[1] representing length.
    coordinates = list(last.exterior.coords)
    coordinates[0] = coordinates[3]
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[1], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[0])))
    coordinates[3] = tuple(x - y for x, y in zip(coordinates[2], (side[1], 0)))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area_rotated = sys.maxsize
    possible_rotated = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[0] < last.bounds[2]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible_rotated:
                possible_rotated = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_top_rotated = translated
                min_area_rotated = ar
        translated = translate(translated, xoff=1.0)

    # Returning the polygon associated with the minimum envelope area.
    if not possible and not possible_rotated:
        return last, -1
    elif not possible and possible_rotated:
        return optimum_top_rotated, min_area_rotated
    elif possible and not possible_rotated:
        return optimum_top, min_area
    else:
        if min_area <= min_area_rotated:
            return optimum_top, min_area
        else:
            return optimum_top_rotated, min_area_rotated

def translate_top_right(last, existing, side):
    # Idea: Place the initial polygon on the right, and in case of equal areas, eveolve towards the top.
    
    # sides[0] representing length and sides[1] representing breadth.
    coordinates = list(last.exterior.coords)
    coordinates[0] = coordinates[1]
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[0], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[1])))
    coordinates[3] = tuple(x + y for x, y in zip(coordinates[0], (0, side[1])))
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
        
    # sides[0] representing breadth and sides[1] representing length.
    coordinates = list(last.exterior.coords)
    coordinates[0] = coordinates[1]
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[1], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[0])))
    coordinates[3] = tuple(x + y for x, y in zip(coordinates[0], (0, side[0])))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area_rotated = sys.maxsize
    possible_rotated = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[1] < last.bounds[3]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible_rotated:
                possible_rotated = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_rt_rotated = translated
                min_area_rotated = ar
        translated = translate(translated, yoff=1.0)
    
    # Returning the polygon associated with the minimum envelope area.
    if not possible and not possible_rotated:
        return last, -1
    elif not possible and possible_rotated:
        return optimum_rt_rotated, min_area_rotated
    elif possible and not possible_rotated:
        return optimum_rt, min_area
    else:
        if min_area <= min_area_rotated:
            return optimum_rt, min_area
        else:
            return optimum_rt_rotated, min_area_rotated

def translate_top_left(last, existing, side):
    # Idea: Place the initial polygon on the right, and in case of equal areas, eveolve towards the bottom.
    
    # sides[0] representing length and sides[1] representing breadth.
    coordinates = list(last.exterior.coords)
    coordinates[3] = coordinates[2]
    coordinates[0] = tuple(x - y for x, y in zip(coordinates[3], (0, side[1])))
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[0], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[1])))
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
        
    # sides[0] representing breadth and sides[1] representing length.
    coordinates = list(last.exterior.coords)
    coordinates[3] = coordinates[2]
    coordinates[0] = tuple(x - y for x, y in zip(coordinates[3], (0, side[0])))
    coordinates[1] = tuple(x + y for x, y in zip(coordinates[0], (side[1], 0)))
    coordinates[2] = tuple(x + y for x, y in zip(coordinates[1], (0, side[0])))
    coordinates[4] = coordinates[0]
    translated = Polygon(coordinates)
    # Translate it by 1.0 in x-direction till there is some overlap of sides.
    min_area_rotated = sys.maxsize
    possible_rotated = False
    # Possible bug: Check for -ve x or y coordinates.
    while translated.bounds[3] > last.bounds[1]:
        if (existing.touches(translated) or existing.disjoint(translated)) and translated.bounds[1] >= 0:
            if not possible_rotated:
                possible_rotated = True
            envelope = unary_union([existing, translated]).bounds
            ar = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
            if ar <= min_area:
                optimum_rb_rotated = translated
                min_area_rotated = ar
        translated = translate(translated, yoff=-1.0)
    
    # Returning the polygon associated with the minimum envelope area.
    if not possible and not possible_rotated:
        return last, -1
    elif not possible and possible_rotated:
        return optimum_rb_rotated, min_area_rotated
    elif possible and not possible_rotated:
        return optimum_rb, min_area
    else:
        if min_area <= min_area_rotated:
            return optimum_rb, min_area
        else:
            return optimum_rb_rotated, min_area_rotated

def plot_masters(placed):
    # Plot the 0th master.
    x, y = placed[0].exterior.xy
    plt.plot(x, y, c="blue")
    x_bot, y_bot = placed[0].bounds[:2]
    plt.annotate(0, (x_bot + 2, y_bot + 2), color="red", ha="center", va="center", fontsize=8)
    last = placed[0]
    for index in range(1, len(placed)):
        current = placed[index]
        x, y = current.exterior.xy
        plt.plot(x, y, c="blue")
        x_bot, y_bot = current.bounds[:2]
        plt.annotate(index, (x_bot + 2, y_bot + 2), color="red", ha="center", va="center", fontsize=8)
        centroid_last = last.centroid
        centroid_current = current.centroid
        x_centroids = [centroid_last.x, centroid_current.x]
        y_centroids = [centroid_last.y, centroid_current.y]
        plt.plot(x_centroids, y_centroids, "k-.")
        last = current
    
def plot_slaves(placed, existing, adj_list, area):
    for index in adj_list:
        master = placed[index]
        slaves = adj_list[index] # A list of [length, breadth] for all the slaves of the master.
        count = "a"
        centroid_master = master.centroid
        for side in slaves:
            candidates = []
            optimum_top, min_top = translate_top(master, existing, side)
            optimum_rt, min_rt = translate_top_right(master, existing, side)
            optimum_bottom, min_bot = translate_bottom(master, existing, side)
            optimum_rb, min_rb = translate_top_left(master, existing, side)
            # Populating candidates for the position for the slave in question.
            if optimum_top.bounds[0] >= 0 and optimum_top.bounds[1] >= 0 and min_top != -1:
                candidates.append(min_top)
            if optimum_rt.bounds[0] >= 0 and optimum_rt.bounds[1] >= 0 and min_rt != -1:
                candidates.append(min_rt)
            if optimum_bottom.bounds[0] >= 0 and optimum_bottom.bounds[1] >= 0 and min_bot != -1:
                candidates.append(min_bot)
            if optimum_rb.bounds[0] >= 0 and optimum_rb.bounds[1] >= 0 and min_rb != -1:
                candidates.append(min_rb)
            candidates.sort()
            if len(candidates) == 0:
                print("Placement of slave with values", side, "for index:", index, "needs manual adjustment!")
                continue
            if candidates[0] == min_top:
                best = optimum_top
                existing = unary_union([existing, optimum_top])
            elif candidates[0] == min_rt:
                best = optimum_rt
                existing = unary_union([existing, optimum_rt])
            elif candidates[0] == min_bot:
                best = optimum_bottom
                existing = unary_union([existing, optimum_bottom])
            else:
                best = optimum_rb
                existing = unary_union([existing, optimum_rb])
            area += best.area
            x, y = best.exterior.xy
            plt.plot(x, y, c="blue")
            x_bot, y_bot = best.bounds[:2]
            plt.annotate(str(index) + count, (x_bot + 2, y_bot + 2), color="red", ha="center", va="center", fontsize=8)
            count = chr(ord(count) + 1)
            centroid_best = best.centroid
            x_centroids = [centroid_master.x, centroid_best.x]
            y_centroids = [centroid_master.y, centroid_best.y]
            plt.plot(x_centroids, y_centroids, "g:")
    return area, existing

def layout(adj_list, anchors, sides):
    # A list of all the polygons, which shall be plotted in the end simultaneously.
    placed = []
    area = 0
    # Assumption: Between consecutive bins, there are atleast two squares.
    existing = Polygon([(0, 0), (sides[0][0], 0), (sides[0][0], sides[0][1]), (0, sides[0][1]), (0, 0)])
    last = existing
    placed.append(last)
    area += last.area
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
            placed.append(last)
            area += last.area
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
            placed.append(last)
            area += last.area
        # Place the envelope separately on the x-axis.
        x_min = last.bounds[0]
        x_max = last.bounds[2]
        side = sides[right_index]
        translated = Polygon([(x_min, 0), (x_min + side[0], 0), (x_min + side[0], side[1]), (x_min, side[1]), (x_min, 0)])
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
        placed.append(last)
        area += last.area
    plot_masters(placed)
    area, existing = plot_slaves(placed, existing, adj_list, area)
    return existing.envelope.area, area

def main():
    """
    Both slaves and masters have been taken to be squares.
    Number the bins so that Bi is close to ith envelope.
    Ex: adj_list = {7: [[2, 4], [2, 4]], ...}
    sides = [[10, 15], [1, 4], ...]
    anchors = [1, 7, 9, ...]
    Keep everything zero-indexed.
    adj_list = {} # A dictionary, where nodes are mapped to their alphabetical slaves' sides' list
    sides = [] # A list of side lengths. sides[i] = [length, breadth] of the ith master.
    anchors = [] # A list of anchors' indices, i.e. squares constrained on the x-axis.
    Ex: adj_list[7] gives all rectangles adjacent to the index = 7 rectangle.
    """
    
    adj_list, sides, anchors = populate({}, [], [])
    plt.tight_layout()
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    envelope_area, area = layout(adj_list, anchors, sides)
    print("Area of the envelope:", envelope_area)
    print("Actual covered area:", float(area))
    print("Area efficiency achieved:", (area * 100) / envelope_area, "%")
    plt.show()

if __name__ == "__main__":
    main()
