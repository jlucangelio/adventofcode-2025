from collections import deque, namedtuple
import copy
import os.path
import typing

input_file = os.path.basename(__file__).split(".")[0] + ".in"
with open(input_file) as f:
    lines = f.read().splitlines()

TEST_INPUT = """.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............""".splitlines()

# diagram = [list(l) for l in TEST_INPUT]
diagram = [list(l) for l in lines]
# print(diagram)

# idx_s = TEST_INPUT[0].index("S")
idx_s = lines[0].index("S")

diagram[1][idx_s] = "|"

splits = 0
for j in range(len(diagram)):
    if j < 2:
        continue

    r = diagram[j]
    for i in range(len(r)):
        p = r[i]
        if diagram[j - 1][i] == "|":
            if p == ".":
                diagram[j][i] = "|"
            if p == "^":
                # print(diagram[j - 1])
                # print("split")
                # Split.
                splits += 1
                if i - 1 >= 0:
                    diagram[j][i - 1] = "|"
                if i + 1 < len(r):
                    diagram[j][i + 1] = "|"

print(splits)


def count_timelines(diagram: list[str], ridx: int, cidx: int, cache) -> int:
    k = (ridx, cidx)
    if k in cache:
        return cache[k]

    if ridx == 0:
        res = 1 if diagram[ridx][cidx] == "S" else 0
        cache[k] = res
        return res

    if ridx == 1:
        res = 1 if diagram[ridx - 1][cidx] == "S" else 0
        cache[k] = res
        return res

    assert(ridx > 1)

    pos = diagram[ridx][cidx]
    parent = diagram[ridx - 1][cidx]

    if pos == ".":
        ntimelines = 0
        if cidx > 0:
            left = diagram[ridx][cidx - 1]
            if left == "^":
                # Beam will split onto this position.
                ntimelines += count_timelines(diagram, ridx, cidx - 1, cache)

        if cidx < len(diagram[0]) - 1:
            right = diagram[ridx][cidx + 1]
            if right == "^":
                # Beam will split onto this position.
                ntimelines += count_timelines(diagram, ridx, cidx + 1, cache)

        if parent == ".":
            # Beam will continue onto this position.
            ntimelines += count_timelines(diagram, ridx - 1, cidx, cache)

        cache[k] = ntimelines
        return ntimelines

    if pos == "^":
        res = count_timelines(diagram, ridx - 1, cidx, cache)
        cache[k] = res
        return res

    assert("Invalid case")
    return 0


diagram = copy.deepcopy(lines)
cache: dict[tuple[int, int], int] = {}
total_count = 0
for cidx in range(len(diagram[-1])):
    ridx = len(diagram) - 1
    # print(ridx, cidx, diagram[ridx][cidx])
    total_count += count_timelines(diagram, ridx, cidx, cache)

print(total_count)
