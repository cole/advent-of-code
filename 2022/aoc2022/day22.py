from dataclasses import dataclass
from io import StringIO
from timeit import default_timer as timer
from typing import Generator, NamedTuple, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_22.txt"


def read_commands(input: str) -> Generator[str | int, None, None]:
    steps = ""
    for char in input:
        match char:
            case "R":
                yield int(steps)
                steps = ""
                yield char
            case "L":
                yield int(steps)
                steps = ""
                yield char
            case _:
                steps += char

    if steps:
        yield int(steps)


class Point(NamedTuple):
    y: int
    x: int


@dataclass
class Heading:
    value: int

    @property
    def facing_score(self) -> int:
        match self.value:
            case 0:
                return 3
            case 90:
                return 0
            case 180:
                return 1
            case 270:
                return 2
            case _:
                raise ValueError(f"Unknown heading: {self.value}")

    def turn_right(self):
        self.value = (self.value + 90) % 360

    def turn_left(self):
        self.value = (self.value - 90) % 360



@dataclass
class Grid:
    rows: list[list[str]]

    def __post_init__(self):
        self._visited = set()
        self._visited_headings = {}

    def __getitem__(self, index: Point) -> str:
        if index.x < 0 or index.y < 0:
            raise IndexError("Let's keep things positive")

        return self.rows[index.y][index.x]

    def mark_visited(self, point: Point, heading: Heading):
        self._visited.add(point)
        self._visited_headings[point] = heading.value

    def get_wrapped_right_point(self, y: int) -> int:
        for x in range(len(self.rows[y])):
            try:
                value = self[Point(y=y, x=x)]
            except IndexError:
                continue
            else:
                if value != " ":
                    return x

    def get_wrapped_left_point(self, y: int) -> int:
        for x in reversed(range(len(self.rows[y]))):
            try:
                value = self[Point(y=y, x=x)]
            except IndexError:
                continue
            else:
                if value != " ":
                    return x

    def get_wrapped_bottom_point(self, x: int) -> int:
        for y in range(len(self.rows)):
            try:
                value = self[Point(y=y, x=x)]
            except IndexError:
                continue
            else:
                if value != " ":
                    return y

    def get_wrapped_top_point(self, x: int) -> int:
        for y in reversed(range(len(self.rows))):
            try:
                value = self[Point(y=y, x=x)]
            except IndexError:
                continue
            else:
                if value != " ":
                    return y

    def print(self, current_position: Point = None):
        for y, row in enumerate(self.rows):
            line = []
            for x, char in enumerate(row):
                point = Point(y=y, x=x)
                if point == current_position:
                    line.append("X")
                elif point in self._visited:
                    if self._visited_headings[point] == 0:
                        line.append("^")
                    elif self._visited_headings[point] == 90:
                        line.append(">")
                    elif self._visited_headings[point] == 180:
                        line.append("v")
                    elif self._visited_headings[point] == 270:
                        line.append("<")
                else:
                    line.append(char)

            print(''.join(line))


def solve_a(input: StringIO) -> int:
    commands = ""
    grid = []
    grid_loaded = False

    for line in input:
        if line == "\n":
            grid_loaded = True
        if grid_loaded:
            commands = line.strip()
        else:
            grid.append([c for c in line.rstrip("\n")])

    grid = Grid(grid)

    position = Point(y=0, x=grid.get_wrapped_right_point(0))
    heading = Heading(90)
    
    for command in read_commands(commands):
        if isinstance(command, int):
            for _ in range(command):
                match heading.value:
                    case 0:
                        next_move = Point(y=position.y - 1, x=position.x)
                    case 90:
                        next_move = Point(y=position.y, x=position.x + 1)
                    case 180:
                        next_move = Point(y=position.y + 1, x=position.x)
                    case 270:
                        next_move = Point(y=position.y, x=position.x - 1)
                    case _:
                        raise ValueError(f"Unknown heading: {heading.value}")

                try:
                    next_move_contents = grid[next_move]
                except IndexError:
                    next_move_contents = " "

                # Wrap around the grid
                if next_move_contents == " ":
                    match heading.value:
                        case 0:
                            next_move = Point(y=grid.get_wrapped_top_point(position.x), x=position.x)
                        case 90:
                            next_move = Point(y=position.y, x=grid.get_wrapped_right_point(position.y))
                        case 180:
                            next_move = Point(y=grid.get_wrapped_bottom_point(position.x), x=position.x)
                        case 270:
                            next_move = Point(y=position.y, x=grid.get_wrapped_left_point(position.y))
                        case _:
                            raise ValueError(f"Unknown heading: {heading.value}")

                if grid[next_move] == "#":
                    pass
                elif grid[next_move] == ".":
                    position = next_move
                    grid.mark_visited(position, heading)

        elif command == "R":
            heading.turn_right()
        elif command == "L":
            heading.turn_left()

    # grid.print(current_position=position)

    return (1000 * (position.y + 1)) + (4 * (position.x + 1)) + heading.facing_score


def solve_b(input: StringIO) -> int:
    return 0


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input)
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input)
    end_b = timer()
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
