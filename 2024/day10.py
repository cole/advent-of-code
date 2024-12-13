import enum
import sys
from typing import NamedTuple

INPUT = open(sys.argv[1]).read().strip()


Point = NamedTuple("Point", [("x", int), ("y", int)])


class Grid:
    def __init__(self, raw_grid):
        self.raw_grid = raw_grid
        self.parsed_grid = []
        for row in raw_grid.split("\n"):
            self.parsed_grid.append([int(c) for c in row])

    def __getitem__(self, point):
        if point.x < 0 or point.x >= self.width:
            raise IndexError(f"X coordinate out of bounds: {point.x}")
        if point.y < 0 or point.y >= self.height:
            raise IndexError(f"Y coordinate out of bounds: {point.y}")

        return self.parsed_grid[point.y][point.x]

    def __iter__(self):
        for y, row in enumerate(self.parsed_grid):
            for x, char in enumerate(row):
                yield Point(x, y), char

    def __contains__(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    @property
    def width(self):
        return len(self.parsed_grid[0]) if self.parsed_grid else 0

    @property
    def height(self):
        return len(self.parsed_grid)

    def rows(self):
        for row in self.parsed_grid:
            yield "".join(row)

    def cols(self):
        for x in range(len(self.parsed_grid[0])):
            yield "".join(row[x] for row in self.parsed_grid)


class Direction(enum.Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)


def get_paths(grid: Grid, start: Point, end: Point):
    queue = [(start, [])]  # start point, empty path
    visited = set()

    paths = []

    while len(queue) > 0:
        point, path = queue.pop(0)
        value = grid[point]
        path.append(point)
        visited.add(point)

        if point == end:
            paths.append(path)

        for direction in Direction:
            adj_point = Point(
                point.x + direction.value[0], point.y + direction.value[1]
            )
            if (
                adj_point in grid
                and adj_point not in visited
                and grid[adj_point] == (value + 1)
            ):
                queue.append((adj_point, path[:]))

    return paths


def part1():
    grid = Grid(INPUT)
    trailheads = set()
    nines = set()
    total_score = 0

    for point, value in grid:
        if value == 0:
            trailheads.add(point)
        if value == 9:
            nines.add(point)

    for point in trailheads:
        for nine in nines:
            try:
                paths = get_paths(grid, point, nine)
            except ValueError:
                continue
            else:
                if paths:
                    total_score += 1

    return total_score


def part2():
    grid = Grid(INPUT)
    trailheads = set()
    nines = set()
    total_score = 0

    for point, value in grid:
        if value == 0:
            trailheads.add(point)
        if value == 9:
            nines.add(point)

    for point in trailheads:
        for nine in nines:
            try:
                paths = get_paths(grid, point, nine)
            except ValueError:
                continue
            else:
                total_score += len(paths)

    return total_score


print(part1())
print(part2())
