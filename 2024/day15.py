import enum
import sys
from typing import NamedTuple

INPUT = open(sys.argv[1]).read().strip()


Point = NamedTuple("Point", [("x", int), ("y", int)])


class Direction(enum.Enum):
    N = enum.auto()
    E = enum.auto()
    S = enum.auto()
    W = enum.auto()


class Grid:
    def __init__(self, raw_grid):
        self.raw_grid = raw_grid
        self.parsed_grid = self.parse_grid(raw_grid)

    def __getitem__(self, point):
        return self.parsed_grid[point.y][point.x]

    def __iter__(self):
        for y, row in enumerate(self.parsed_grid):
            for x, char in enumerate(row):
                yield Point(x, y), char

    def parse_grid(self, raw_grid):
        return [list(row) for row in raw_grid.split("\n")]

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

    def print(self):
        for row in self.parsed_grid:
            print("".join(row))

    def move(self, start, direction) -> Point:
        match direction:
            case "^":
                dest = Point(start.x, start.y - 1)
            case ">":
                dest = Point(start.x + 1, start.y)
            case "v":
                dest = Point(start.x, start.y + 1)
            case "<":
                dest = Point(start.x - 1, start.y)
            case _:
                raise ValueError(f"Invalid direction: {direction}")

        if not (0 <= dest.x < self.width and 0 <= dest.y < self.height):
            return start

        start_char = self[start]
        dest_char = self[dest]
        if dest_char == "#":
            return start
        elif dest_char == "O":
            if self.move(dest, direction) == dest:
                # box can't be pushed
                return start

        self.parsed_grid[dest.y][dest.x] = start_char
        self.parsed_grid[start.y][start.x] = "."

        return dest


def part1():
    raw_grid, moves = INPUT.split("\n\n")
    grid = Grid(raw_grid)
    start_point = [point for point, char in grid if char == "@"][0]

    current_pos = start_point
    for move in moves:
        if move == "\n":
            continue
        current_pos = grid.move(current_pos, move)

    coordinate_total = 0
    for point, char in grid:
        if char == "O":
            coordinate_total += point.x + (point.y * 100)

    return coordinate_total


def part2():
    raw_grid, moves = INPUT.split("\n\n")
    grid = []
    for row in raw_grid.split("\n"):
        line = []
        for char in row:
            if char == "@":
                line.extend(["@", "."])
            elif char == "O":
                line.extend(["[", "]"])
            else:
                line.extend([char, char])
        grid.append(line)
    moves = moves.replace("\n", "")

    start = None
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "@":
                start = (x, y)
                break

    directions = {
        "^": (0, -1),
        ">": (1, 0),
        "v": (0, 1),
        "<": (-1, 0),
    }

    current = start
    for move in moves:
        move_x, move_y = directions[move]

        waiting = []
        queue = [current]
        can_move = True
        while can_move and len(queue) > 0:
            cx, cy = queue.pop(0)
            dx, dy = cx + move_x, cy + move_y

            if grid[dy][dx] == "#":
                can_move = False
                break

            if grid[dy][dx] in ("[", "]"):
                queue.append((dx, dy))
                if move in ("^", "v"):
                    offset = 1 if grid[dy][dx] == "[" else -1
                    queue.append((dx + offset, dy))

            waiting.append(((cx, cy), (dx, dy)))

        if can_move:
            moved = set()
            for (sx, sy), (dx, dy) in reversed(waiting):
                if ((sx, sy), (dx, dy)) in moved:
                    continue

                grid[dy][dx] = grid[sy][sx]
                grid[sy][sx] = "."

                if grid[dy][dx] == "@":
                    current = (dx, dy)

                moved.add(((sx, sy), (dx, dy)))

    # print("\n".join(r for r in ["".join(row) for row in grid]))

    coordinate_total = 0
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char == "[":
                coordinate_total += x + (y * 100)

    return coordinate_total


print(part1())
print(part2())
