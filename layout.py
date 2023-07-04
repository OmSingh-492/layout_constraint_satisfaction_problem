import sys
from shapely.geometry import Polygon, box
from shapely.affinity import translate
from shapely.ops import unary_union
import matplotlib.pyplot as plt

def populate(adj_list, sides, anchors):
    # FILL IN WITH METHOD TO POPULATE THE DATA STRUCTURES. KEEP INTEGRAL SIDE LENGTHS.
    adj_list = {}
    sides = [[15, 25], [10, 20], [20, 30], [80, 100], [15, 35], [12, 22], [25, 50], [15, 25], [20, 30], [20, 40]]
    anchors = [0, 3, 6, 9]
    return adj_list, sides, anchors

def create_envelopes(adj_list, sides):
    # Create an envelope for master-slaves, to pack the envelopes later instead of actual squares.
    for rect in adj_list.keys():
        slaves = adj_list[rect]
        side_master = sides[int(rect[1])][0]
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
        sides[int(rect[1])] = [side_master, side]
    # First function which should be ran for creating envelopes.
    return adj_list, sides

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

def plot(last, current, index):
    # A generic plotting function.
    x, y = current.exterior.xy
    plt.plot(x, y, c="blue")
    x_bot, y_bot = current.bounds[:2]
    plt.annotate(index, (x_bot + 2, y_bot + 2), color="red", ha="center", va="center", fontsize=8)
    centroid_last = last.centroid
    centroid_current = current.centroid
    x_centroids = [centroid_last.x, centroid_current.x]
    y_centroids = [centroid_last.y, centroid_current.y]
    plt.plot(x_centroids, y_centroids, "k--", label="Related")

def layout(anchors, sides):
    # Assumption: Between consecutive bins, there are atleast two squares.
    existing = Polygon([(0, 0), (sides[0][0], 0), (sides[0][0], sides[0][1]), (0, sides[0][1]), (0, 0)])
    prev = existing
    last = existing
    # Plot the polygon
    plot(prev, last, 0)
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
            plot(prev, last, index)
            prev = last
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
            plot(prev, last, index)
            prev = last
        # Place the envelope separately on the x-axis. Use red colour for its borders.
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
        # Plot the polygon.
        plot(prev, last, right_index)
        prev = last

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
    Improvements:
    We consider all the masters and slaves are still squares as before, but to reduce clearance between 
    squares, we consider that envelopes can be rectangles as well. Now, sides is a list of lists [length, breadth].
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
