import os.path

# TEST_INPUT = """L68
# L30
# R48
# L5
# R60
# L55
# L1
# L99
# R14
# L82
# """.splitlines()

input_file = os.path.basename(__file__).split(".")[0] + ".in"

LEN = 100
pos = 50
part1_count = 0
part2_count = 0

with open(input_file) as f:
    for line in f:
    # for line in TEST_INPUT:
        # print(line.strip())
        steps = int(line[1:])
        # print("steps", steps)

        # Every full circle will click on 0 once.
        part2_count += (steps // LEN)
        # print("part2", part2_count)

        if line[0] == "L":
            steps = -steps

        new_pos = (pos + steps) % LEN
        # print("previous", pos, steps, "new", new_pos)

        # If we end up in 0, count.
        if new_pos == 0:
            part1_count += 1
            part2_count += 1
            pos = new_pos
            continue

        # Did we click through 0?
        # move right
        if pos > 0 and steps > 0 and new_pos < pos:
            part2_count += 1
            # print("added one")
        if pos > 0 and steps < 0 and new_pos > pos:
            part2_count += 1
            # print("added one")

        pos = new_pos

print("part 1", part1_count)
print("part 2", part2_count)
