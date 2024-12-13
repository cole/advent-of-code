import enum
import sys
from typing import NamedTuple

INPUT = open(sys.argv[1]).read().strip()
SAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE"""

Point = NamedTuple("Point", [("x", int), ("y", int)])


class Grid:
    def __init__(self, raw_grid):
        self.raw_grid = raw_grid
        self.parsed_grid = []
        for row in raw_grid.split("\n"):
            self.parsed_grid.append([c for c in row])

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


class Plot:
    def __init__(self, char: str):
        self.char = char
        self.points = set()

    @classmethod
    def from_grid(cls, grid: Grid, start: Point):
        char = grid[start]
        queue = [start]

        plot = cls(char)
        checked = set()

        while len(queue) > 0:
            next_point = queue.pop(0)
            if next_point in checked:
                continue

            checked.add(next_point)
            plot.points.add(next_point)

            for direction in Direction:
                adj_point = Point(
                    next_point.x + direction.value[0],
                    next_point.y + direction.value[1],
                )
                if adj_point in grid and grid[adj_point] == char:
                    queue.append(adj_point)

        return plot

    def __contains__(self, point):
        return point in self.points

    @property
    def area(self):
        return len(self.points)

    @property
    def perimeter(self):
        sides = 0
        for point in self.points:
            for direction in Direction:
                adj_point = Point(
                    point.x + direction.value[0],
                    point.y + direction.value[1],
                )
                if adj_point not in self:
                    sides += 1

        return sides

    @property
    def sides(self):
        edge_points = {}
        for point in self.points:
            for direction in Direction:
                adj_point = Point(
                    point.x + direction.value[0],
                    point.y + direction.value[1],
                )
                if adj_point not in self:
                    edge_points[point].setdefault([])
                    edge_points[point].append(adj_point)

        for point, adj_points in edge_points.items():
            pass

        return sides


def part1():
    grid = Grid(INPUT)
    unvisited = set([point for point, _ in grid])
    total = 0

    while unvisited:
        point = unvisited.pop()
        plot = Plot.from_grid(grid, point)
        unvisited.difference_update(plot.points)
        total += plot.area * plot.perimeter

    return total


def part2():
    grid = Grid(SAMPLE)
    unvisited = set([point for point, _ in grid])
    total = 0

    while unvisited:
        point = unvisited.pop()
        plot = Plot.from_grid(grid, point)
        unvisited.difference_update(plot.points)
        total += plot.area * plot.sides

    return total


print(part1())
print(part2())
