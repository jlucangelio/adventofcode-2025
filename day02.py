import os.path

def count_part1(s_id):
    if len(s_id) % 2 == 1:
        # Odd-length ids cannot be invalid.
        return False

    l = len(s_id) // 2
    return 1 if s_id[:l] == s_id[l:] else 0


def count_part2(s_id):
    length = len(s_id)
    for l in range(1, length // 2 + 1):
        if length % l != 0:
            continue

        reps = length // l
        if s_id[:l] * reps == s_id:
            return 1

    return 0


TEST_INPUT = """11-22,95-115,998-1012,1188511880-1188511890,
222220-222224,1698522-1698528,446443-446449,38593856-38593862,
565653-565659,824824821-824824827,2121212118-2121212124"""

input_file = os.path.basename(__file__).split(".")[0] + ".in"

with open(input_file) as f:
    line = f.readline()

id_ranges = [tuple([int(n) for n in r.split("-")]) for r in  line.split(",")]
# id_ranges = [tuple([int(n) for n in r.split("-")]) for r in TEST_INPUT.split(",")]
print(id_ranges)

count1 = 0
count2 = 0
for b, e in id_ranges:
    for p_id in range(b, e + 1):
        # print(p_id)

        s_id = str(p_id)
        count1 += count_part1(s_id) * p_id
        count2 += count_part2(s_id) * p_id

print("part 1", count1)
print("part 2", count2)
