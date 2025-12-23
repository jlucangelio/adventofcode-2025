import os.path
import typing

TEST_INPUT = """987654321111111
811111111111119
234234234234278
818181911112111""".splitlines()

input_file = os.path.basename(__file__).split(".")[0] + ".in"

with open(input_file) as f:
    lines = f.readlines()


def make_joltage(batteries: list[int], cache, start_idx: int, ndigits: int):
    assert(start_idx < len(batteries))
    assert(start_idx + ndigits <= len(batteries))

    # print(batteries)
    # print("start", start_idx, "ndigits", ndigits)

    if (start_idx, ndigits) in cache:
        jolts = cache[(start_idx, ndigits)]
        return (jolts, str(jolts))

    # Ran out of digits.
    if ndigits == 0:
        return (0, "")

    # At this point we have enough batteries left for the digits required.
    if ndigits == 1:
        m = max(batteries[start_idx:])
        return (m, str(m))

    # Need to choose all batteries that are left.
    if start_idx + ndigits == len(batteries):
        remainder = "".join(str(n) for n in batteries[start_idx:])
        return (int(remainder), remainder)

    max_jolts = 0
    suffix = batteries[start_idx:]
    max_digit = max(suffix[:-ndigits + 1])
    max_digit_idx = start_idx + suffix.index(max_digit)
    rem_digits = ndigits - 1

    for idx in range(max_digit_idx + 1, len(batteries) - rem_digits + 1):
        n, s = make_joltage(batteries, cache, idx, rem_digits)
        jolts = max_digit * 10**len(s) + n
        if jolts > max_jolts:
            max_jolts = jolts

    cache[(start_idx, ndigits)] = max_jolts
    return (max_jolts, str(max_jolts))


res1 = 0
res2 = 0
for bank in lines:
    # print(bank)
    batteries = list([int(n) for n in str(bank.strip())])
    # print(batteries)

    j, _ = make_joltage(batteries, {}, 0, 2)
    # print("part 1", j)
    res1 += j
    j, _ = make_joltage(batteries, {}, 0, 12)
    # print("part 2", j)
    res2 += j

print(res1)
print(res2)
