import sys

INPUT = open(sys.argv[1]).read().strip()

# INPUT = """467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598.."""

grid = [list(line) for line in INPUT.splitlines()]


def check_surrounds(y, x_start, x_end):
    above, below, left, right = [], [], [], []
    if y > 0:
        above = [grid[y - 1][xa] for xa in range(x_start, x_end)]
        if x_start > 0:
            above = [grid[y - 1][x_start - 1]] + above

        try:
            above = above + [grid[y - 1][x_end]]
        except IndexError:
            pass

    if y < (len(grid) - 1):
        below = [grid[y + 1][xa] for xa in range(x_start, x_end)]

        if x_start > 0:
            below = [grid[y + 1][x_start - 1]] + below

        try:
            below = below + [grid[y + 1][x_end]]
        except IndexError:
            pass

    if x_start > 0:
        left = [grid[y][x_start - 1]]

    try:
        right = [grid[y][x_end]]
    except IndexError:
        right = []

    return any([not (c == "." or c.isnumeric()) for c in above + below + left + right])


def part1():
    part_numbers = []
    for y, line in enumerate(grid):
        num_len = 0
        for x, c in enumerate(line):
            if c.isnumeric():
                num_len += 1
            else:
                if num_len:
                    if check_surrounds(y, x - num_len, x):
                        part_numbers.append(int("".join(grid[y][x - num_len : x])))
                num_len = 0

        if num_len:
            x_start = x - num_len + 1
            x_end = x + 1
            if check_surrounds(y, x_start, x_end):
                part_numbers.append(int("".join(grid[y][x_start:x_end])))

    return sum(part_numbers)


def surrounds(y, x):
    surrounds = [
        (y - 1, x - 1),
        (y - 1, x),
        (y - 1, x + 1),
        (y, x - 1),
        (y, x),
        (y, x + 1),
        (y + 1, x - 1),
        (y + 1, x),
        (y + 1, x + 1),
    ]
    max_y = len(grid) - 1
    max_x = len(grid[0]) - 1

    return [
        s
        for s in surrounds
        if (s[0] >= 0 and s[0] <= max_y and s[1] >= 0 and s[1] <= max_x)
    ]


def number(y, x):
    start = x
    end = x
    max_x = len(grid[0]) - 1
    while True:
        if start == 0:
            break

        before = grid[y][start - 1]
        if before.isnumeric():
            start -= 1
        else:
            break

    while True:
        if end == max_x:
            break

        after = grid[y][end + 1]
        if after.isnumeric():
            end += 1
        else:
            break

    return y, (start, end + 1)


def part2():
    gear_ratios = []

    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c == "*":
                all_adjacent = surrounds(y, x)
                adjacent_numbers = [
                    coord
                    for coord in all_adjacent
                    if grid[coord[0]][coord[1]].isnumeric()
                ]
                number_positions = set(
                    [number(coord[0], coord[1]) for coord in adjacent_numbers]
                )
                if len(number_positions) == 2:
                    gear_ratios.append(
                        tuple(
                            [
                                int(
                                    "".join(
                                        grid[num_pos[0]][num_pos[1][0] : num_pos[1][1]]
                                    )
                                )
                                for num_pos in number_positions
                            ]
                        )
                    )
    return sum([gear[0] * gear[1] for gear in gear_ratios])


print(f"1: {part1()}")
print(f"2: {part2()}")
