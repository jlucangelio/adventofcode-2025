from collections import namedtuple
import copy
import os.path
import typing

TEST_INPUT = """..@@.@@@@.
@@@.@.@.@@
@@@@@.@.@@
@.@@@@..@.
@@.@@@@.@@
.@@@@@@@.@
.@.@.@.@@@
@.@@@.@@@@
.@@@@@@@@.
@.@.@@@.@.""".splitlines()

input_file = os.path.basename(__file__).split(".")[0] + ".in"

with open(input_file) as f:
    lines = f.read().splitlines()

Direction = namedtuple("Direction", "x y")
Position = namedtuple("Position", "c r")

UP = Direction(0, -1)
DOWN = Direction(0, 1)
LEFT = Direction(-1, 0)
RIGHT = Direction(1, 0)

def add_direction(d1, d2):
    return Direction(d1.x + d2.x, d1.y + d2.y)


def move(p, d):
    return Position(p.c + d.x, p.r + d.y)

UPLEFT =  add_direction(UP, LEFT)
UPRIGHT = add_direction(UP, RIGHT)
DOWNLEFT = add_direction(DOWN, LEFT)
DOWNRIGHT = add_direction(DOWN, RIGHT)

directions = [UP, DOWN, LEFT, RIGHT, UPLEFT, UPRIGHT, DOWNLEFT, DOWNRIGHT]

diagram = lines
# diagram = TEST_INPUT
nrows = len(diagram)
ncols = len(diagram[0])
total_count = 0

for j in range(0, nrows):
    for i in range(0, ncols):
        if diagram[j][i] != "@":
            continue

        p = Position(i, j)
        single_count = 0
        for d in directions:
            p2 = move(p, d)
            if p2.r < 0 or p2.c < 0 or p2.r >= nrows or p2.c >= ncols:
                continue

            if diagram[p2.r][p2.c] == "@":
                single_count += 1

        if single_count < 4:
            total_count += 1

print("part 1", total_count)

diagram = [list(r) for r in lines]
# diagram = [list(r) for r in TEST_INPUT]
total_removed = 0
nremoved = 1
while nremoved > 0:
    next_diagram = copy.deepcopy(diagram)
    nremoved = 0

    for j in range(0, nrows):
        for i in range(0, ncols):
            if diagram[j][i] != "@":
                continue

            p = Position(i, j)
            single_count = 0
            for d in directions:
                p2 = move(p, d)
                if p2.r < 0 or p2.c < 0 or p2.r >= nrows or p2.c >= ncols:
                    continue

                if diagram[p2.r][p2.c] == "@":
                    single_count += 1

            if single_count < 4:
                next_diagram[j][i] = "."
                nremoved += 1


    print("removed ", nremoved)
    total_removed += nremoved
    diagram = next_diagram

print("part 2", total_removed)
