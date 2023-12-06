import sys
from math import prod

INPUT = open(sys.argv[1]).read().strip()


def part1():
    times, distances = INPUT.splitlines()
    races = []
    for time, distance in zip(
        times.lstrip("Time:").strip().split(),
        distances.lstrip("Distance:").strip().split(),
    ):
        races.append((int(time), int(distance)))

    winners = []
    for time, distance in races:
        w = 0
        for hold in range(1, time - 1):
            travelled = (time - hold) * hold
            if travelled > distance:
                w += 1

        winners.append(w)

    return prod(winners)


def part2():
    times, distances = INPUT.splitlines()
    time = int("".join(times.lstrip("Time:").strip().split()))
    distance = int("".join(distances.lstrip("Distance:").strip().split()))
    w = 0
    for hold in range(1, time - 1):
        travelled = (time - hold) * hold
        if travelled > distance:
            w += 1

    return w


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
