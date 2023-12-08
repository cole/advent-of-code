import itertools
import sys
from math import gcd, prod

INPUT = open(sys.argv[1]).read().strip()

lines = INPUT.splitlines()

sequence = lines[0]
paths = {}
for line in lines[2:]:
    start, rest = line.split("=")
    left, right = rest.split(",")

    paths[start.strip()] = (left.lstrip(" ("), right.rstrip(")").strip())


def part1():
    location = "AAA"
    steps = 0
    while location != "ZZZ":
        for char in sequence:
            steps += 1
            if char == "R":
                location = paths[location][1]
            else:
                location = paths[location][0]

            if location == "ZZZ":
                break

    return steps


def step(starts):
    locations = starts
    while True:
        for char in sequence:
            index = 0 if char == "L" else 1
            locations = tuple([paths[loc][index] for loc in locations])

            yield locations


def part2():
    starts = tuple([k for k in paths.keys() if k.endswith("A")])
    steps = 0

    loc_steps = [None for _ in starts]
    for locations in step(starts):
        steps += 1
        for i, loc in enumerate(locations):
            if loc.endswith("Z") and loc_steps[i] is None:
                loc_steps[i] = steps

        if all(loc_steps):
            gcds = []
            for x, y in itertools.combinations(loc_steps, 2):
                gcds.append(gcd(x, y))

            assert len(set(gcds)) == 1
            return prod([s // gcds[0] for s in loc_steps]) * gcds[0]


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
