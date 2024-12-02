import collections
import sys

INPUT = open(sys.argv[1]).read().strip()

parsed = [tuple(map(int, line.split())) for line in INPUT.split("\n")]


def part1():
    first = sorted(item[0] for item in parsed)
    second = sorted(item[1] for item in parsed)

    total = 0
    for left, right in zip(first, second):
        total += max(left, right) - min(left, right)

    return total


def part2():
    first = sorted(item[0] for item in parsed)
    second = collections.Counter(item[1] for item in parsed)

    total = 0
    for item in first:
        total += item * second[item]

    return total


print(part1())
print(part2())
