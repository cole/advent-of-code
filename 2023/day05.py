import sys

INPUT = open(sys.argv[1]).read().strip()


class Map:
    def __init__(self, name, ranges):
        self.name = name
        values = []
        for line in ranges:
            values.append(self.parse_line(line))

        values.sort(key=lambda s: s[0] + s[2])

        self.values = values

    def __str__(self):
        return f"{self.name} {self.values}"

    def __iter__(self):
        return iter(self.values)

    def parse_line(self, line):
        ds, ss, r = [int(v) for v in line.split(" ")]
        se = ss + r
        offset = ds - ss
        return (ss, se, offset)

    def forwards(self, position):
        for start, end, offset in self.values:
            if start <= position < end:
                return position + offset

        return position

    def backwards(self, position):
        for start, end, offset in self.values:
            if start + offset <= position < end + offset:
                return position - offset

        return position


class Seeds:
    def __init__(self, seeds):
        seeds = [int(s) for s in seeds.lstrip("seeds: ").split(" ")]
        seed_map = []
        i = 0
        while i < len(seeds):
            ss, sr = seeds[i], seeds[i + 1]
            seed_map.append((ss, ss + sr))
            i += 2

        self.values = seed_map

    def __contains__(self, item):
        for start, end in self.values:
            if start <= item < end:
                return True

        return False


def part1():
    maps = []
    sections = INPUT.split("\n\n")

    seeds = [int(s) for s in sections[0].lstrip("seeds: ").split(" ")]
    for section in sections:
        name, *ranges = section.splitlines()
        maps.append(Map(name, ranges))

    positions = seeds.copy()
    for map in maps:
        positions = [map.forwards(seed) for seed in positions]

    return min(positions)


def part2():
    sections = INPUT.split("\n\n")

    seeds = Seeds(sections[0])
    maps = []

    for section in sections[1:]:
        name, *ranges = section.splitlines()
        maps.append(Map(name, ranges))

    reverse_maps = list(reversed(maps))

    # Just gave up on a proper solution :(
    for location in range(50_000_000, 200_000_000):
        position = location
        for map in reverse_maps:
            position = map.backwards(position)

        if position in seeds:
            return location

    raise ValueError("not found")


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
