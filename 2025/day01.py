import sys

INPUT = open(sys.argv[1]).read().strip()


def stop_positions(input):
    dial = range(100)
    position = 50
    yield dial[position]
    for instruction in input:
        sign = -1 if instruction[0] == "L" else 1
        steps = int(instruction[1:])
        position += sign * steps
        yield dial[position % len(dial)]


def all_positions(input):
    dial = range(100)
    position = 50
    for instruction in input:
        sign = -1 if instruction[0] == "L" else 1
        steps = int(instruction[1:])
        movement = sign * steps
        last = None
        for point in range(position + sign, position + movement + sign, sign):
            yield dial[point % len(dial)]
            last = point

        position = last % len(dial)


def part1():
    return len(
        [position for position in stop_positions(INPUT.split("\n")) if position == 0]
    )


def part2():
    return len(
        [position for position in all_positions(INPUT.split("\n")) if position == 0]
    )


print(part1())
print(part2())
