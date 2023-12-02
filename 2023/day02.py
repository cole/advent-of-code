import sys

INPUT = open(sys.argv[1]).read().strip()

games = {}
for id, line in enumerate(INPUT.splitlines(), start=1):
    games[id] = {}
    _, sets = line.split(":")
    subsets = sets.split(";")
    for subset in subsets:
        subsubsets = subset.split(",")
        for subsubset in subsubsets:
            number, color = subsubset.strip().split(" ")
            games[id].setdefault(color, 0)
            games[id][color] = max(games[id][color], int(number))


def part1():
    required = {
        "red": 12,
        "green": 13,
        "blue": 14,
    }

    ids = []
    for id, cubes in games.items():
        if all([cubes[color] <= required[color] for color in required.keys()]):
            ids.append(id)

    print(sum(ids))


def part2():
    powers = []
    for _, cubes in games.items():
        power = cubes["red"] * cubes["blue"] * cubes["green"]
        powers.append(power)

    print(sum(powers))


part1()
part2()
