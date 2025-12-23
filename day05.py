from collections import deque, namedtuple
import os.path
import typing

input_file = os.path.basename(__file__).split(".")[0] + ".in"
with open(input_file) as f:
    lines = f.read().splitlines()

TEST_INPUT = """3-5
10-14
16-20
12-18

1
5
8
11
17
32""".splitlines()

ranges = []
ingredients: list[int] = []
doing_ranges = True
for line in lines:
# for line in TEST_INPUT:
    if line == "":
        doing_ranges = False
        continue

    if doing_ranges:
        ranges.append(tuple([int(n) for n in line.split("-")]))
    else:
        ingredients.append(int(line))

# print(ranges)
# print(ingredients)

nfresh = 0
for ing in ingredients:
    for b, e in ranges:
        if ing >= b and ing <= e:
            nfresh += 1
            break

print("part 1", nfresh)

total_fresh = 0

Range = namedtuple("Range", "begin end")


def ranges_disjoint(a: Range, b: Range) -> bool:
    return a.end < b.begin or a.begin > b.end


def all_disjoint(ranges: deque[Range]) -> bool:
    l = len(ranges)
    for i, ri in enumerate(ranges):
        for j, rj in enumerate(ranges):
            if i != j:
                # print(ri, rj)
                if not ranges_disjoint(ri, rj):
                    return False
    return True


def make_disjoint(a: Range, b: Range) -> tuple[bool, list[Range]]:
    if a.end < b.begin or a.begin > b.end:
        # Already disjoint.
        return (False, [a, b])

    if a == b:
        return (True, [a])

    if a.begin < b.begin and a.end <= b.end:
        # A and B overlap, so merge them.
        return (True, [Range(a.begin, b.end)])

    if a.begin >= b.begin and a.end > b.end:
        # A and B overlap, so merge them.
        return (True, [Range(b.begin, a.end)])

    if a.begin > b.begin and a.end < b.end:
        # A is fully included in B.
        return (True, [b])

    if a.begin < b.begin and b.end < a.end:
        # B is fully included in A.
        return (True, [a])

    assert("missing case")
    return (False, [a, b])


def range_union(a: Range, b: Range) -> list[Range]:
    if a.end < b.begin or a.begin > b.end:
        # A does not overlap B
        return [a, b]

    if a.begin >= b.begin and a.end <= b.end:
        # A is fully included in B
        return [b]

    if a.begin <= b.begin and b.end <= a.end:
        # B is fully included in A.
        return [a]

    if a.begin >= b.begin and a.end > b.end:
        return [Range(b.begin, a.end)]

    if a.begin < b.begin and a.end <= b.end:
        return [Range(a.begin, b.end)]

    assert("Missing case")
    return []


def range_count(a: Range):
    return a.end - a.begin + 1


ranges = [Range(b, e) for b, e in ranges]
zero_overlaps: list[Range] = []
global_overlaps: dict[int, list[int]] = {}
final_ranges: list[Range] = []
ranges_remaining: set[int] = set(range(len(ranges)))

for i, ri in enumerate(ranges):
    overlaps: list[int] = []
    for j, rj in enumerate(ranges):
        if i != j:
            if not ranges_disjoint(ri, rj):
                overlaps.append(j)

    if len(overlaps) == 0:
        zero_overlaps.append(ri)
        ranges_remaining.remove(i)
    else:
        global_overlaps[i] = overlaps

print(len(zero_overlaps))
print(len(ranges_remaining))

# print(global_overlaps)

for idx, overlaps in global_overlaps.items():
    # print(idx)
    if idx not in ranges_remaining:
        continue

    q: deque[int] = deque([idx])
    overlapping_ranges: set[int] = set()

    while (len(q) > 0):
        # print("q", q)
        j = q.popleft()
        # print("j", j)
        if j not in ranges_remaining:
            continue
        overlapping_ranges.add(j)
        q.extend(global_overlaps[j])
        ranges_remaining.remove(j)

    minb = ranges[idx].begin
    maxe = ranges[idx].end

    for range_idx in overlapping_ranges:
        r = ranges[range_idx]
        minb = min(minb, r.begin)
        maxe = max(maxe, r.end)

    final_ranges.append(Range(minb, maxe))


print("zero overlaps", zero_overlaps)
print("final ranges", final_ranges)

final_count = 0
for z in zero_overlaps:
    final_count += range_count(z)

for f in final_ranges:
    final_count += range_count(f)

print("part 2", final_count)
