import enum
import sys

INPUT = open(sys.argv[1]).read().strip()


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)


class Heading(enum.StrEnum):
    N = "^"
    E = ">"
    S = "v"
    W = "<"


class Grid:
    def __init__(self, raw_grid):
        self.raw_grid = raw_grid
        self.parsed_grid = [list(row) for row in raw_grid.split("\n")]

    def __getitem__(self, point):
        return self.parsed_grid[point.y][point.x]

    def __iter__(self):
        for y, row in enumerate(self.parsed_grid):
            for x, char in enumerate(row):
                yield Point(x, y), char


class Guard:
    def __init__(self, current_point, heading):
        self.current_point = current_point
        self.heading = heading

    def next_move(self, grid):
        match self.heading:
            case Heading.N:
                return Point(self.current_point.x, self.current_point.y - 1)
            case Heading.E:
                return Point(self.current_point.x + 1, self.current_point.y)
            case Heading.S:
                return Point(self.current_point.x, self.current_point.y + 1)
            case Heading.W:
                return Point(self.current_point.x - 1, self.current_point.y)

    def turn(self):
        if self.heading == Heading.N:
            self.heading = Heading.E
        elif self.heading == Heading.E:
            self.heading = Heading.S
        elif self.heading == Heading.S:
            self.heading = Heading.W
        elif self.heading == Heading.W:
            self.heading = Heading.N


GRID = Grid(INPUT)


def part1():
    visited = set()
    initial_pos = None
    for point, char in GRID:
        if char == "^":
            initial_pos = point
            break

    guard = Guard(initial_pos, Heading.N)

    while True:
        next_point = guard.next_move(GRID)
        try:
            next_pos_char = GRID[next_point]
        except IndexError:
            visited.add(guard.current_point)
            break

        if next_pos_char == "#":
            guard.turn()
            continue

        visited.add(guard.current_point)
        guard.current_point = next_point

    return len(visited)


def part2():
    possible_points = set()
    loop_points = set()

    initial_guard_pos = None
    for point, char in GRID:
        if char == "^":
            initial_guard_pos = point
        elif char == ".":
            possible_points.add(point)

    for i, obstacle in enumerate(possible_points):
        if i % 1000 == 0:
            print(f"Checked point index {i}/{len(possible_points)}")
        visited = set()
        guard = Guard(initial_guard_pos, Heading.N)

        while True:
            next_point = guard.next_move(GRID)

            if (next_point, guard.heading) in visited:
                loop_points.add(obstacle)
                break

            if next_point.x < 0 or next_point.y < 0:
                visited.add((guard.current_point, guard.heading))
                break

            try:
                next_pos_char = GRID[next_point]
            except IndexError:
                visited.add((guard.current_point, guard.heading))
                break

            if next_point == obstacle or next_pos_char == "#":
                visited.add((guard.current_point, guard.heading))
                guard.turn()
                continue

            visited.add((guard.current_point, guard.heading))
            guard.current_point = next_point

    return len(loop_points)


print(part1())
print(part2())
