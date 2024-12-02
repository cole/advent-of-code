import sys

INPUT = open(sys.argv[1]).read().strip()
PARSED = [tuple(map(int, line.split())) for line in INPUT.split("\n")]


def validate(row):
    prev = None
    row_increasing = None
    safe = True
    for idx, val in enumerate(row[1:], 1):
        prev = row[idx - 1]
        increasing = val > prev
        if row_increasing is None:
            row_increasing = increasing
        elif row_increasing != increasing:
            safe = False
            break

        diff = abs(val - prev)
        if not (1 <= diff <= 3):
            safe = False
            break

    return safe


def part1():
    safe_count = 0
    for row in PARSED:
        if validate(row):
            safe_count += 1
    return safe_count


def part2():
    safe_count = 0
    for row in PARSED:
        if validate(row):
            safe_count += 1
        else:
            for idx in range(len(row)):
                removed_level = row[:idx] + row[idx + 1 :]
                if validate(removed_level):
                    safe_count += 1
                    break

    return safe_count


print(part1())
print(part2())
