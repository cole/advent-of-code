import sys

INPUT = open(sys.argv[1]).read().strip()


def part1():
    fresh_ranges = []
    for range in INPUT.split("\n\n")[0].strip().split("\n"):
        start, end = range.split("-")
        fresh_ranges.append((int(start), int(end)))

    ingredient_ids = [int(i) for i in INPUT.split("\n\n")[1].strip().split("\n")]

    freshies = 0
    for ingredient in ingredient_ids:
        for range_start, range_end in fresh_ranges:
            if range_start <= ingredient <= range_end:
                freshies += 1
                break

    return freshies


def consolidate(ranges):
    consolidated = set()
    sorted_ranges = sorted(ranges, key=lambda v: v[0])
    start, end = None, None
    for range_start, range_end in sorted_ranges:
        if start is None:
            start = range_start
        if end is None:
            end = range_end

        if end < range_start:
            # gap
            consolidated.add((start, end))
            start = range_start
            end = range_end
        else:
            # continue
            end = max(end, range_end)

    consolidated.add((start, end))

    return sorted(list(consolidated), key=lambda v: v[0])


def part2():
    fresh_ranges = []
    for range_str in INPUT.split("\n\n")[0].strip().split("\n"):
        start, end = range_str.split("-")
        fresh_ranges.append((int(start), int(end)))

    total = 0
    for start, end in consolidate(fresh_ranges):
        total += end - start + 1

    return total


print(f"part1: {part1()}")
print(f"part2: {part2()}")
