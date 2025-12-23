from collections import deque, namedtuple
import os.path
import typing

input_file = os.path.basename(__file__).split(".")[0] + ".in"
with open(input_file) as f:
    content = f.read().splitlines()
    lines = [line.split() for line in content]

TEST_INPUT = """123 328  51 640
 45 64  387 230
  6 98  215 314
*   +   *   +  """.splitlines()

lines = [line.split() for line in TEST_INPUT]

ncols = len(lines[0])
nrows = len(lines)

# print(lines)
total = 0
for col in range(ncols):
    res = 0
    if lines[-1][col] == "+":
        res = sum([int(lines[i][col]) for i in range(nrows - 1)])
    elif lines[-1][col] == "*":
        res = 1
        [res := res * int(lines[i][col]) for i in range(nrows - 1)]

    total += res

print(total)

grand_total = 0
# content = TEST_INPUT
print(content)

separator_idxs: list[int] = []

for i, c in enumerate(content[-1]):
    if c != " ":
        separator_idxs.append(i)

print(separator_idxs)
for i, idx in enumerate(separator_idxs):

    b = idx
    if i < len(separator_idxs) - 1:
        e = separator_idxs[i + 1] - 1
    else:
        e = len(content[0])

    total = 0
    if content[-1][b] == "+":
        total = 0
        f = lambda a, b: a + b
    elif content[-1][b] == "*":
        total = 1
        f = lambda a, b: a * b
    else:
        assert()

    for jdx in range(b, e):
        n = int("".join([r[jdx] for r in content[:-1]]))
        total = f(total, n) # type: ignore

    grand_total += total
    print(total)

print(grand_total)
