import sys

INPUT = open(sys.argv[1]).read().strip()


def rotate90(matrix):
    return [list(row[::-1]) for row in zip(*matrix)]


def tilt(grid, direction="N"):
    # Just rotate first, then do a north tilt
    if direction == "S":
        grid = rotate90(grid)
        grid = rotate90(grid)
    elif direction == "W":
        grid = rotate90(grid)
    elif direction == "E":
        grid = rotate90(grid)
        grid = rotate90(grid)
        grid = rotate90(grid)

    for y, row in enumerate(grid):
        if y == 0:
            continue

        for x, c in enumerate(row):
            if c != "O":
                continue

            yf = y
            move_to = None
            while True:
                yf = yf - 1
                try:
                    dv = grid[yf][x]
                except IndexError:
                    break

                if dv == ".":
                    move_to = yf, x
                else:
                    break

                if yf == 0:
                    break

            if move_to:
                grid[move_to[0]][move_to[1]] = "O"
                grid[y][x] = "."

    # reverse prior rotation
    if direction == "S":
        grid = rotate90(grid)
        grid = rotate90(grid)

    elif direction == "W":
        grid = rotate90(grid)
        grid = rotate90(grid)
        grid = rotate90(grid)
    elif direction == "E":
        grid = rotate90(grid)

    return grid


def spin(grid):
    grid = tilt(grid, direction="N")
    grid = tilt(grid, direction="W")
    grid = tilt(grid, direction="S")
    grid = tilt(grid, direction="E")

    return grid


def calc_load(grid):
    height = len(grid)
    total = 0
    for y, line in enumerate(grid):
        rocks = [c for c in line if c == "O"]
        total += len(rocks) * (height - y)

    return total


def part1():
    g = [list(l) for l in INPUT.splitlines()]
    tilt(g)

    return calc_load(g)


def part2():
    g = [list(l) for l in INPUT.splitlines()]

    for _ in range(1000):
        g = spin(g)

    return calc_load(g)


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
