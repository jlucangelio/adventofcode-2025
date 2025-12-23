from collections import defaultdict, deque, namedtuple
import copy
import itertools
import math
import os.path
import typing

input_file = os.path.basename(__file__).split(".")[0] + ".in"
with open(input_file) as f:
    lines = f.read().splitlines()

TEST_INPUT = """[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}""".splitlines()

# lines = TEST_INPUT

def toggle(lights: list[bool], press: list[int]) -> None:
    for idx in press:
        lights[idx] = not lights[idx]


def find_configuration(npresses: int, buttons: list[list[int]], target: list[bool],
                       sequence: list[int]):
    if npresses == 0:
        lights = [False for _ in target]
        for press in sequence:
            toggle(lights, buttons[press])
        # print("lights", lights)
        # print("target", lights)
        return lights == target

    found = False
    for button in range(len(buttons)):
        sequence.append(button)
        if find_configuration(npresses - 1, buttons, target, sequence):
            found = True
        sequence.pop()

    return found

presses_per_line = [0 for _ in lines]
all_found = [False for _ in lines]
total_found = 0

targets_per_line = []
buttons_per_line = []
for i, line in enumerate(lines):
    splits = line.split()
    targets_per_line.append([t == "#" for t in splits[0][1:-1]])
    buttons_per_line.append([[int(l) for l  in b[1:-1].split(",")]
                             for b in splits[1:-1]])

for max_presses in range(1, 1000):
    for i, line in enumerate(lines):
        if all_found[i]:
            continue

        buttons = buttons_per_line[i]
        targets = targets_per_line[i]

        # print(target_lights, buttons)

        for npresses in range(1, max_presses + 1):
            if find_configuration(npresses, buttons, targets, []):
                print(i, "requires", npresses)
                all_found[i] = True
                presses_per_line[i] = npresses
                total_found += 1
                break

    if all(all_found):
        print("part1", sum(presses_per_line))
        break
    else:
        print("have", total_found, "of", len(lines))
        print("need more presses")

print()

import sympy
from sympy.abc import * # type: ignore

vars = [a, b, c, d, e, f, g, h, i, j, k, l, m]

final_count = 0
for line in lines:
    print(line)
    splits = line.split()
    buttons = [[int(l) for l in b[1:-1].split(",")]
               for b in splits[1:-1]]
    joltages = [int(j) for j in splits[-1][1:-1].split(",")]
    # print(buttons)
    # print(joltages)
    min_counters_per_button = min([len(b) for b in buttons])
    counters_per_button = [len(b) for b in buttons]
    total_joltages = sum(joltages)

    counters_to_buttons = defaultdict(list)
    for button_idx, counter_list in enumerate(buttons):
        for counter in counter_list:
            counters_to_buttons[counter].append(button_idx)

    equations = []
    for counter, cbuttons in counters_to_buttons.items():
        exp = sympy.Add(*[vars[b] for b in cbuttons])
        exp = exp - joltages[counter]
        equations.append(exp)

    solvevars = [a, b, c, d, e, f, g, h, i, j, k, l, m][:len(buttons)]
    sorted_joltages = sorted(joltages)
    upper_bounds = {}
    ranges = []
    for idx, v in enumerate(solvevars):
        affected_counters = buttons[idx]
        relevant_targets = [joltages[c] for c in affected_counters]
        upper_bounds[v] = min(relevant_targets) + 1

    # print(upper_bounds)
    # print(solvevars)

    solutions = sympy.solve(equations, solvevars, dict=True)
    free_vars = []
    for var in vars[:len(buttons)]:
        if var not in solutions[0].keys():
            free_vars.append(var)

    print("free vars", free_vars)
    for var in free_vars:
        ranges.append(range(upper_bounds[var]))

    solution = solutions[0]
    if len(free_vars) == 0:
        presses = sum(solution.values())
        print(presses, "presses")
        final_count += presses
    else:
        print(equations)
        print(solution)
        functions = []
        for s in solution.values():
            func = sympy.utilities.lambdify(free_vars, s)
            functions.append(func)

        min_presses = total_joltages
        min_assignment = None
        for var_assignment in itertools.product(*ranges):
            total_presses = 0
            sum_assignments = sum(var_assignment)

            for func in functions:
                formula_presses = func(*var_assignment)
                if formula_presses < -0.001:
                    break
                if abs(formula_presses - round(formula_presses)) > 0.001:
                    break
                total_presses += round(formula_presses)
            else:
                total_presses += sum_assignments
                min_presses = min(total_presses, min_presses)
                if min_presses == total_presses:
                    min_assignment = copy.copy(var_assignment)

        # print(min_presses)
        assert(min_assignment is not None)

        print("assignment", min_assignment)
        print(min_presses, "presses")
        final_count += min_presses

    print()

print(final_count)
