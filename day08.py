from collections import deque, namedtuple
import copy
import math
import os.path
import typing

input_file = os.path.basename(__file__).split(".")[0] + ".in"
with open(input_file) as f:
    lines = f.read().splitlines()

TEST_INPUT = """162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689""".splitlines()


JunctionBox = namedtuple("JunctionBox", "x y z")
Connection = namedtuple("Connection", "v1, v2")


def distance(jb1: JunctionBox, jb2: JunctionBox):
    return math.sqrt((jb1.x - jb2.x)**2 + (jb1.y - jb2.y)**2 + (jb1.z - jb2.z)**2)


jbs = []
jb_ids = {}
# for i, line in enumerate(TEST_INPUT):
for i, line in enumerate(lines):
    x, y, z = line.split(",")
    jb = JunctionBox(int(x), int(y), int(z))
    jbs.append(jb)
    jb_ids[i] = jb

distances: list[tuple[float, int, int]] = []
for i, jb1 in enumerate(jbs):
    for j, jb2 in enumerate(jbs):
        if i < j:
            distances.append((distance(jb1, jb2), i, j))

distances.sort(key=lambda t: t[0])
part2_distances = copy.copy(distances)
# print(distances)
print("distances done")

# part 1

jb_circuits: dict[int, int] = {}
circuits: dict[int, set[int]] = {}
next_id = 0
# for step in range(10):
for step in range(1000):
    if step % 100 == 0:
        print("step ", step)

    d, id1, id2 = distances[step]

    if id1 not in jb_circuits and id2 not in jb_circuits:
        jb_circuits[id1] = next_id
        jb_circuits[id2] = next_id
        circuits[next_id] = set([id1, id2])
        next_id += 1

    if id1 in jb_circuits and id2 not in jb_circuits:
        circ_id = jb_circuits[id1]
        jb_circuits[id2] = jb_circuits[id1]
        circuits[circ_id].add(id2)

    if id2 in jb_circuits and id1 not in jb_circuits:
        circ_id = jb_circuits[id2]
        jb_circuits[id1] = jb_circuits[id2]
        circuits[circ_id].add(id1)

    if id1 in jb_circuits and id2 in jb_circuits:
        circ1_id = jb_circuits[id1]
        circ2_id = jb_circuits[id2]

        if circ1_id == circ2_id:
            continue

        circ1_len = len(circuits[circ1_id])
        circ2_len = len(circuits[circ2_id])

        if circ1_len > circ2_len:
            update_to_id = circ1_id
            update_from_id = circ2_id
        else:
            update_to_id = circ2_id
            update_from_id = circ1_id

        update_from = circuits[update_from_id]
        for jb_id in update_from:
            jb_circuits[jb_id] = update_to_id
        circuits[update_to_id].update(update_from)

sizes = [len(v) for v in circuits.values()]
sizes.sort(reverse=True)
print("part 1", sizes[0] * sizes[1] * sizes[2])

# part 2

jb_circuits: dict[int, int] = {}
circuits: dict[int, set[int]] = {}
next_id = 0
step = 0
x_product = 0
circ_len = 0
while circ_len < len(jb_ids):
    if step % 1000 == 0:
        print("step ", step)

    d, id1, id2 = distances[step]
    step += 1

    jb1 = jb_ids[id1]
    jb2 = jb_ids[id2]
    x_product = jb1.x * jb2.x

    if id1 not in jb_circuits and id2 not in jb_circuits:
        jb_circuits[id1] = next_id
        jb_circuits[id2] = next_id
        circuits[next_id] = set([id1, id2])
        circ_len = 2
        next_id += 1

    if id1 in jb_circuits and id2 not in jb_circuits:
        circ_id = jb_circuits[id1]
        jb_circuits[id2] = jb_circuits[id1]
        circuits[circ_id].add(id2)
        circ_len = len(circuits[circ_id])

    if id2 in jb_circuits and id1 not in jb_circuits:
        circ_id = jb_circuits[id2]
        jb_circuits[id1] = jb_circuits[id2]
        circuits[circ_id].add(id1)
        circ_len = len(circuits[circ_id])

    if id1 in jb_circuits and id2 in jb_circuits:
        circ1_id = jb_circuits[id1]
        circ2_id = jb_circuits[id2]

        if circ1_id == circ2_id:
            continue

        circ1_len = len(circuits[circ1_id])
        circ2_len = len(circuits[circ2_id])

        if circ1_len > circ2_len:
            update_to_id = circ1_id
            update_from_id = circ2_id
        else:
            update_to_id = circ2_id
            update_from_id = circ1_id

        update_from = circuits[update_from_id]
        for jb_id in update_from:
            jb_circuits[jb_id] = update_to_id
        circuits[update_to_id].update(update_from)
        del circuits[update_from_id]

        circ_len = circ1_len + circ2_len

print("steps", step)
print("part 2", x_product)
