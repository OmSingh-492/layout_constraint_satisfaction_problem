import operator, sys
from random import randint
from shapely.geometry import Polygon, box
from shapely.ops import unary_union
import matplotlib.pyplot as plt

def plot_polygon(p, n, t):
  x, y = p.exterior.xy
  plt.plot(x, y, c="blue")
  plt.annotate(n, xy=t)

def bottom_right(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[2] = new_vertices[1]
  new_vertices[3] = tuple(map(operator.sub, new_vertices[2], (side, 0)))
  new_vertices[0] = tuple(map(operator.sub, new_vertices[3], (0, side)))
  new_vertices[1] = tuple(map(operator.add, new_vertices[0], (side, 0)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def bottom_left(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[3] = new_vertices[0]
  new_vertices[0] = tuple(map(operator.sub, new_vertices[3], (0, side)))
  new_vertices[1] = tuple(map(operator.add, new_vertices[0], (side, 0)))
  new_vertices[2] = tuple(map(operator.add, new_vertices[1], (0, side)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def right_down(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[0] = new_vertices[1]
  new_vertices[1] = tuple(map(operator.add, new_vertices[0], (side, 0)))
  new_vertices[2] = tuple(map(operator.add, new_vertices[1], (0, side)))
  new_vertices[3] = tuple(map(operator.add, new_vertices[0], (0, side)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def right_up(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[3] = new_vertices[2]
  new_vertices[0] = tuple(map(operator.sub, new_vertices[3], (0, side)))
  new_vertices[1] = tuple(map(operator.add, new_vertices[0], (side, 0)))
  new_vertices[2] = tuple(map(operator.add, new_vertices[1], (0, side)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def left_bottom(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[1] = new_vertices[0]
  new_vertices[2] = tuple(map(operator.add, new_vertices[1], (0, side)))
  new_vertices[3] = tuple(map(operator.sub, new_vertices[2], (side, 0)))
  new_vertices[0] = tuple(map(operator.sub, new_vertices[3], (0, side)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def left_up(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[2] = new_vertices[3]
  new_vertices[1] = tuple(map(operator.sub, new_vertices[2], (0, side)))
  new_vertices[0] = tuple(map(operator.sub, new_vertices[1], (side, 0)))
  new_vertices[3] = tuple(map(operator.add, new_vertices[0], (0, side)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def top_right(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[1] = new_vertices[2]
  new_vertices[2] = tuple(map(operator.add, new_vertices[1], (0, side)))
  new_vertices[3] = tuple(map(operator.sub, new_vertices[2], (side, 0)))
  new_vertices[0] = tuple(map(operator.sub, new_vertices[3], (0, side)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def top_left(last_added, existing, side):
  new_vertices = list(last_added.exterior.coords)
  new_vertices[0] = new_vertices[3]
  new_vertices[1] = tuple(map(operator.add, new_vertices[0], (side, 0)))
  new_vertices[2] = tuple(map(operator.add, new_vertices[1], (0, side)))
  new_vertices[3] = tuple(map(operator.sub, new_vertices[2], (side, 0)))
  new_vertices[4] = new_vertices[0]
  if existing.touches(Polygon(new_vertices)) or existing.disjoint(Polygon(new_vertices)):
    envelope = unary_union([existing, Polygon(new_vertices)]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      return Polygon(new_vertices), -1
    area = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
    return Polygon(new_vertices), area
  else:
    return Polygon(new_vertices), -1

def get_fixed(x_bl, side):
  return Polygon([(x_bl, 0), (x_bl + side, 0), (x_bl + side, side), (x_bl, side), (x_bl, 0)])

def find_plot(lengths):
  existing = Polygon([(0, 0), (lengths[0], 0), (lengths[0], lengths[0]), (0, lengths[0]), (0, 0)])
  last_added = existing
  plot_polygon(existing, 0, (0, 0))
  count = 1
  n = len(lengths)
  for side_length in lengths[1:(n - 1)]:
    areas = []
    br, area = bottom_right(last_added, existing, side_length)
    areas += [area]
    bl, area = bottom_left(last_added, existing, side_length)
    areas += [area]
    rd, area = right_down(last_added, existing, side_length)
    areas += [area]
    ru, area = right_up(last_added, existing, side_length)
    areas += [area]
    lb, area = left_bottom(last_added, existing, side_length)
    areas += [area]
    lu, area = left_up(last_added, existing, side_length)
    areas += [area]
    tr, area = top_right(last_added, existing, side_length)
    areas += [area]
    tl, area = top_left(last_added, existing, side_length)
    areas += [area]
    choice = -1
    min = sys.maxsize
    for i in range(8):
      if areas[i] != -1 and areas[i] < min:
        choice = i
        min = areas[i]
    if choice == 0:
      existing = unary_union([existing, br])
      last_added = br
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(br, count, t)
    elif choice == 1:
      existing = unary_union([existing, bl])
      last_added = bl
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(bl, count, t)
    elif choice == 2 or choice == -1:
      existing = unary_union([existing, rd])
      last_added = rd
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(rd, count, t)
      if choice == -1:
        print(f"Square number {count} needs to be adjusted manually later on!")
    elif choice == 3:
      existing = unary_union([existing, ru])
      last_added = ru
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(ru, count, t)
    elif choice == 4:
      existing = unary_union([existing, lb])
      last_added = lb
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(lb, count, t)
    elif choice == 5:
      existing = unary_union([existing, lu])
      last_added = lu
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(lu, count, t)
    elif choice == 6:
      existing = unary_union([existing, tr])
      last_added = tr
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(tr, count, t)
    else:
      existing = unary_union([existing, tl])
      last_added = tl
      t = (list(last_added.exterior.coords))[0]
      plot_polygon(tl, count, t)
    count += 1
  x_min, x_max = last_added.bounds[0], last_added.bounds[2]
  left = get_fixed(x_min, lengths[-1])
  right = get_fixed(x_max, lengths[-1])
  area_l = area_r = 0 
  if existing.touches(left) or existing.disjoint(left):
    envelope = unary_union([existing, left]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      area_l = sys.maxsize
    area_l = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
  else:
    area_l = sys.maxsize
  if existing.touches(right) or existing.disjoint(right):
    envelope = unary_union([existing, right]).bounds
    if envelope[0] < 0 or envelope[1] < 0:
      area_r = sys.maxsize
    area_r = box(envelope[0], envelope[1], envelope[2], envelope[3]).area
  else:
    area_r = sys.maxsize
  if area_r <= area_l:
    existing = unary_union([existing, right])
    last_added = right
    t = (list(last_added.exterior.coords))[0]
    plot_polygon(right, count, t)
  else:
    existing = unary_union([existing, left])
    last_added = left
    t = (list(last_added.exterior.coords))[0]
    plot_polygon(left, count, t)
  count += 1
  envelope = existing.bounds
  return box(envelope[0], envelope[1], envelope[2], envelope[3]).area

def main():
  n = int(input("Enter the number of squares: "))
  min, max = map(int, input("Enter the minimum and maximum possible side lengths: ").split())
  lengths = []
  net = 0
  for i in range(n):
    side = randint(min, max)
    lengths += [side]
    net += side * side
  plt.rcParams["figure.figsize"] = [50.0, 50.0]
  plt.rcParams["figure.autolayout"] = True
  ax = plt.gca()
  ax.set_aspect('equal', adjustable='box')
  print("Side lengths:", lengths)
  efficiency = net / find_plot(lengths)
  print("In all the cases, slide the fixed square on the x-axis manually, if there are no fixed squares.")
  print("Area Efficiency:", efficiency)
  plt.show()

if __name__ == "__main__":
  main()
