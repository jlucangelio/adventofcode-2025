from collections import deque, namedtuple
import copy
import math
import os.path
import typing

input_file = os.path.basename(__file__).split(".")[0] + ".in"
with open(input_file) as f:
    lines = f.read().splitlines()

TEST_INPUT = """7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3""".splitlines()

Point = namedtuple("Point", "x y")
Rect = namedtuple("Rect", "c1 c2")

def point_from_str(s: str):
    return Point(*[int(c) for c in s.split(",")])

def area(c1: Point, c2: Point) -> int:
    return ((max(c1.x, c2.x) - min(c1.x, c2.x) + 1) *
            (max(c1.y, c2.y) - min(c1.y, c2.y) + 1))

def rarea(r: Rect) -> int:
    return area(r.c1, r.c2)

points = []
# for line in TEST_INPUT:
for line in lines:
    points.append(point_from_str(line))

# print(points)
max_area = 0
for i, pi in enumerate(points):
    for j, pj in enumerate(points):
        if i < j:
            max_area = max(max_area, area(pi, pj))

print("part 1", max_area)

RED = 0
GREEN = 1
dpoints: dict[Point, int] = {}

# lines = TEST_INPUT
for i, line in enumerate(lines):
    cur = point_from_str(line)
    next = point_from_str(lines[(i + 1) % len(lines)])

    # print(cur, next)

    dpoints[cur] = RED
    if cur.x == next.x:
        for j in range(min(cur.y + 1, next.y), max(cur.y, next.y)):
            dpoints[Point(cur.x, j)] = GREEN
    elif cur.y == next.y:
        for i in range(min(cur.x + 1, next.x), max(cur.x, next.x)):
            dpoints[Point(i, cur.y)] = GREEN
    else:
        assert()

    # print(next)
    dpoints[next] = RED

# print(dpoints)

# max_area = 0
# for i, pi in enumerate(points):
#     for j, pj in enumerate(points):
#         if i < j:
#             # if only green tiles
#             max_area = max(max_area, area(pi, pj))
