import sys
from typing import NamedTuple

INPUT = open(sys.argv[1]).read().strip()

Point = NamedTuple("Point", [("x", int), ("y", int)])


class Map:
    def __init__(self, raw_grid):
        self.raw_grid = raw_grid
        self.parsed_grid = [list(row) for row in raw_grid.split("\n")]

    def __getitem__(self, point):
        return self.parsed_grid[point.y][point.x]

    def __iter__(self):
        for y, row in enumerate(self.parsed_grid):
            for x, char in enumerate(row):
                yield Point(x, y), char

    @property
    def width(self):
        return len(self.parsed_grid[0]) if self.parsed_grid else 0

    @property
    def height(self):
        return len(self.parsed_grid)

    def is_valid(self, point):
        return 0 <= point.x < self.width and 0 <= point.y < self.height

    def rows(self):
        for row in self.parsed_grid:
            yield "".join(row)

    def cols(self):
        for x in range(len(self.parsed_grid[0])):
            yield "".join(row[x] for row in self.parsed_grid)

    def print(self, points=None):
        for y, row in enumerate(self.parsed_grid):
            for x, char in enumerate(row):
                if points and Point(x, y) in points:
                    print("X", end="")
                else:
                    print(char, end="")
            print()


def get_antinodes(point_a, point_b, map):
    x_diff = abs(point_a.x - point_b.x)
    y_diff = abs(point_a.y - point_b.y)

    if point_a.y > point_b.y:
        point_a_antinode_y = point_a.y + y_diff
        point_b_antinode_y = point_b.y - y_diff
    else:
        point_b_antinode_y = point_b.y + y_diff
        point_a_antinode_y = point_a.y - y_diff

    if point_a.x > point_b.x:
        point_a_antinode_x = point_a.x + x_diff
        point_b_antinode_x = point_b.x - x_diff
    else:
        point_b_antinode_x = point_b.x + x_diff
        point_a_antinode_x = point_a.x - x_diff

    point_a_antinode = None
    if point_a_antinode_x >= 0 and point_a_antinode_y >= 0:
        point_a_antinode = Point(point_a_antinode_x, point_a_antinode_y)
        try:
            map[point_a_antinode]
        except IndexError:
            pass

    point_b_antinode = None
    if point_b_antinode_x >= 0 and point_b_antinode_y >= 0:
        point_b_antinode = Point(point_b_antinode_x, point_b_antinode_y)
        try:
            map[point_b_antinode]
        except IndexError:
            pass

    return point_a_antinode, point_b_antinode


def project_points(point_a, point_b, step=1):
    x_diff = abs(point_a.x - point_b.x) * step
    y_diff = abs(point_a.y - point_b.y) * step

    if point_a.y > point_b.y:
        top_point, bottom_point = point_b, point_a
    else:
        top_point, bottom_point = point_a, point_b

    if point_a.x > point_b.x:
        left_point, right_point = point_b, point_a
    else:
        left_point, right_point = point_a, point_b

    if top_point == left_point:
        yield (
            Point(top_point.x - x_diff, top_point.y - y_diff),
            Point(bottom_point.x + x_diff, bottom_point.y + y_diff),
        )
    else:
        yield (
            Point(left_point.x - x_diff, left_point.y + y_diff),
            Point(right_point.x + x_diff, right_point.y - y_diff),
        )

    yield from project_points(point_a, point_b, step + 1)


def part1():
    map = Map(INPUT)
    antenna_types = set(INPUT)
    antenna_types.remove(".")
    antenna_types.remove("\n")

    antinodes = set()

    for antenna_type in antenna_types:
        antenna_points = set()

        for point, char in map:
            if char == antenna_type:
                antenna_points.add(point)

        for point_a in antenna_points:
            for point_b in [p for p in antenna_points if p != point_a]:
                point_a_antinode, point_b_antinode = get_antinodes(
                    point_a, point_b, map
                )
                if point_a_antinode:
                    antinodes.add(point_a_antinode)
                if point_b_antinode:
                    antinodes.add(point_b_antinode)

    return len(antinodes)


def part2():
    map = Map(INPUT)
    antenna_types = set(INPUT)
    antenna_types.remove(".")
    antenna_types.remove("\n")

    antinodes = set()

    for antenna_type in antenna_types:
        antenna_points = set()

        for point, char in map:
            if char == antenna_type:
                antenna_points.add(point)

        for point_a in antenna_points:
            for point_b in [p for p in antenna_points if p != point_a]:
                antinodes.add(point_a)
                antinodes.add(point_b)

                for point_a_antinode, point_b_antinode in project_points(
                    point_a, point_b
                ):
                    if point_a_antinode and map.is_valid(point_a_antinode):
                        antinodes.add(point_a_antinode)
                    if point_b_antinode and map.is_valid(point_b_antinode):
                        antinodes.add(point_b_antinode)

                    if not (
                        point_a_antinode and map.is_valid(point_a_antinode)
                    ) and not (point_b_antinode and map.is_valid(point_b_antinode)):
                        break

    return len(antinodes)


print(part1())
print(part2())
