import sys

INPUT = open(sys.argv[1]).read().strip()


def get_accessible_rolls(grid):
    matching_points = []

    for y, line in enumerate(grid):
        for x, char in enumerate(line):
            if char != "@":
                continue

            adjacent_points = [
                (x - 1, y - 1),
                (x, y - 1),
                (x + 1, y - 1),
                (x - 1, y),
                (x + 1, y),
                (x - 1, y + 1),
                (x, y + 1),
                (x + 1, y + 1),
            ]
            adjacent_points = [p for p in adjacent_points if p[0] >= 0 and p[1] >= 0]
            adjacent_rolls = []
            for adj_x, adj_y in adjacent_points:
                try:
                    if grid[adj_y][adj_x] == "@":
                        adjacent_rolls.append((adj_x, adj_y))
                except IndexError:
                    pass

            if len(adjacent_rolls) < 4:
                matching_points.append((x, y))

    return matching_points


def part1():
    grid = []
    for line in INPUT.split("\n"):
        grid.append(list(line))

    return len(get_accessible_rolls(grid))


def part2():
    grid = []
    for line in INPUT.split("\n"):
        grid.append(list(line))

    next_pass = get_accessible_rolls(grid)
    removed = 0
    while next_pass:
        for x, y in next_pass:
            grid[y][x] = "."
            removed += 1

        next_pass = get_accessible_rolls(grid)

    return removed


print(f"part1: {part1()}")
print(f"part2: {part2()}")
