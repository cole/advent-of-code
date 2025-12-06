import operator
import sys
from functools import reduce

INPUT = open(sys.argv[1]).read().strip()


def part1():
    grid = []
    for line in INPUT.strip().split("\n"):
        row = []
        for item in line.split():
            row.append(item)
        grid.append(row)

    total = 0
    height = len(grid)

    for x, _ in enumerate(grid[0]):
        problems = [int(grid[y][x]) for y in range(height - 1)]
        if grid[height - 1][x] == "*":
            op = operator.mul
            initial = 1
        elif grid[height - 1][x] == "+":
            op = operator.add
            initial = 0
        else:
            raise ValueError(f"unknown op {grid[height][x]}")

        result = reduce(op, problems, initial)

        # print(f"problems: {problems} op: {op} result: {result}")
        total += result

    return total


def part2():
    grid = []
    for line in INPUT.strip().split("\n"):
        grid.append(line)

    width = max([len(row) for row in grid])
    height = len(grid)

    total = 0

    col_starts = []
    for index, chr in enumerate(grid[len(grid) - 1]):
        if chr != " ":
            col_starts.append(index)

    for index, col_start in enumerate(col_starts):
        try:
            next_start = col_starts[index + 1]
        except IndexError:
            next_start = width

        problem = []
        for col_index in reversed(range(col_start, next_start)):
            value = ""
            for row_index in range(len(grid) - 1):
                try:
                    value += grid[row_index][col_index]
                except IndexError:
                    pass

            try:
                problem.append(int(value.strip()))
            except ValueError:
                pass

        if grid[height - 1][col_start] == "*":
            op = operator.mul
            initial = 1
        elif grid[height - 1][col_start] == "+":
            op = operator.add
            initial = 0
        else:
            raise ValueError(f"unknown op {grid[height - 1][col_start]}")

        result = reduce(op, problem, initial)

        # print(f"problem: {problem} op: {op} result: {result}")
        total += result

    return total


print(f"part1: {part1()}")
print(f"part2: {part2()}")
