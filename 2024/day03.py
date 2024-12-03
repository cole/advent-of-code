import re
import sys

INPUT = open(sys.argv[1]).read().strip()


def part1():
    total = 0
    for op in re.findall(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", INPUT):
        total += int(op[0]) * int(op[1])
    return total


def split_conditionals(input):
    pos = 0
    enabled = True
    while pos < len(input):
        if enabled:
            try:
                next_stop = input.index("don't()", pos)
            except ValueError:
                yield input[pos:]
                break
            else:
                yield input[pos:next_stop]

            pos = next_stop + 7
            enabled = False
        else:
            try:
                next_start = input.index("do()", pos)
            except ValueError:
                break
            else:
                pos = next_start + 3
                enabled = True


def part2():
    total = 0

    for line in split_conditionals(INPUT):
        for op in re.findall(r"mul\(([0-9]{1,3}),([0-9]{1,3})\)", line):
            total += int(op[0]) * int(op[1])

    return total


print(part1())
print(part2())
