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
    def edge_points(self):
        edge_points = set()
        for point in self.points:
            for direction in Direction:
                adj_point = Point(
                    point.x + direction.value[0],
                    point.y + direction.value[1],
                )
                if adj_point not in self:
                    edge_points.add(point)

        return edge_points

    @property
    def perimeter(self):
        return len(self.edge_points)

    @property
    def sides(self):
        count = 0
        seen = {
            Direction.UP: set(),
            Direction.RIGHT: set(),
            Direction.DOWN: set(),
            Direction.LEFT: set(),
        }

        edge_points = self.edge_points

        for point in edge_points:
            for direction in Direction:
                adj_point = Point(
                    point.x + direction.value[0],
                    point.y + direction.value[1],
                )
                if adj_point in self:
                    continue
                if adj_point in seen[direction]:
                    continue

                seen[direction].add(adj_point)

                next_low, next_high = adj_point, adj_point
                if direction in (Direction.UP, Direction.DOWN):
                    while (
                        next_low not in self
                        and Point(next_low.x, next_low.y - direction.value[1]) in self
                    ):
                        seen[direction].add(next_low)
                        next_low = Point(next_low.x - 1, next_low.y)

                    while (
                        next_high not in self
                        and Point(next_high.x, next_high.y - direction.value[1]) in self
                    ):
                        seen[direction].add(next_high)
                        next_high = Point(next_high.x + 1, next_high.y)
                else:
                    while (
                        next_low not in self
                        and Point(next_low.x - direction.value[0], next_low.y) in self
                    ):
                        seen[direction].add(next_low)
                        next_low = Point(next_low.x, next_low.y - 1)

                    while (
                        next_high not in self
                        and Point(next_high.x - direction.value[0], next_high.y) in self
                    ):
                        seen[direction].add(next_high)
                        next_high = Point(next_high.x, next_high.y + 1)

                count += 1

        return count


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
    grid = Grid(INPUT)
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
