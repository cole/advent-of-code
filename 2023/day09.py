import itertools
import sys


INPUT = open(sys.argv[1]).read().strip()


def extrapolate(sequence):
    level = sequence
    levels = [level]
    while not all([v == 0 for v in level]):
        level = [b - a for a, b in itertools.pairwise(level)]
        levels.append(level)

    v = 0
    for level in reversed(levels):
        v = v + level[-1]

    return v


def part1():
    total = 0
    for line in INPUT.splitlines():
        total += extrapolate([int(v) for v in line.split()])

    return total


def extrapolate_backwards(sequence):
    level = sequence
    levels = [level]
    while not all([v == 0 for v in level]):
        next_level = [b - a for a, b in itertools.pairwise(level)]
        level = next_level
        levels.append(level)

    v = 0
    for level in reversed(levels):
        v = level[0] - v

    return v


def part2():
    total = 0
    for line in INPUT.splitlines():
        total += extrapolate_backwards([int(v) for v in line.split()])

    return total


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
