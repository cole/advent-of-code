from dataclasses import dataclass
from io import StringIO
from timeit import default_timer as timer
from typing import Literal, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_14.txt"

Air = Literal["."]
Sand = Literal["o"]
Rock = Literal["#"]


@dataclass
class Grid:
    rows: Tuple[Tuple[Air | Rock | Sand, ...]]
    has_floor: bool = False

    @classmethod
    def parse(cls, input: StringIO, add_floor: bool = False) -> "Grid":
        rock_points = set()
        for line in input:
            current_x, current_y = None, None
            for line_point in line.split(" -> "):
                next_x, next_y = line_point.strip().split(",")
                next_x, next_y = int(next_x), int(next_y)

                new_points = []
                if current_x and current_x == next_x:
                    min_y = min(current_y, next_y)
                    max_y = max(current_y, next_y)
                    new_points = [(current_x, y) for y in range(min_y, max_y + 1)]
                elif current_y and current_y == next_y:
                    min_x = min(current_x, next_x)
                    max_x = max(current_x, next_x)
                    new_points = [(x, current_y) for x in range(min_x, max_x + 1)]
                elif current_x or current_y:
                    raise ValueError(f"diagonal line {line_point}")

                rock_points.update(new_points)

                current_x, current_y = next_x, next_y

        max_x = max([x for x, _ in rock_points])
        max_y = max([y for _, y in rock_points])

        grid = [["." for _ in range(0, max_x + 1)] for _ in range(0, max_y + 1)]
        for x, y in rock_points:
            grid[y][x] = "#"

        if add_floor:
            # Also extend grid 200 to the right
            for row in grid:
                row.extend(["." for _ in range(200)])
            grid.append(["." for _ in range(0, max_x + 201)])
            grid.append(["#" for _ in range(0, max_x + 201)])

        return cls(rows=tuple([tuple(row) for row in grid]), has_floor=add_floor)

    def print(self):
        for row in self.rows:
            print("".join(row[450:]))

    def add_sand(self, start_x: int, start_y: int) -> "Grid":
        at_rest = False
        if self.rows[start_y][start_x] != ".":
            return self, False

        sand_position = start_x, start_y
        while not at_rest:
            try:
                down = self.rows[sand_position[1] + 1][sand_position[0]]
            except IndexError:
                # Fell off the grid
                sand_position = None, None
                break

            if down == ".":
                sand_position = sand_position[0], sand_position[1] + 1
                continue

            at_floor = self.has_floor and sand_position[1] == len(self.rows) - 1
            if at_floor:
                # Floor is infinite, so can't go diagonally off the grid.
                break

            # Sand or rock, move down and left
            try:
                down_and_left = self.rows[sand_position[1] + 1][sand_position[0] - 1]
            except IndexError:
                # Fell off the grid
                sand_position = None, None
                break

            if down_and_left == ".":
                sand_position = sand_position[0] - 1, sand_position[1] + 1
                continue

            # Sand or rock, move down and left
            try:
                down_and_right = self.rows[sand_position[1] + 1][sand_position[0] + 1]
            except IndexError:
                # Fell off the grid
                sand_position = None, None
                break

            if down_and_right == ".":
                sand_position = sand_position[0] + 1, sand_position[1] + 1
                continue

            at_rest = True

        if sand_position == (None, None):
            return self, False

        new_rows = []
        for index, row in enumerate(self.rows):
            if sand_position[1] == index:
                updated_row = list(row)
                updated_row[sand_position[0]] = "o"
                new_rows.append(tuple(updated_row))
            else:
                new_rows.append(row)

        return Grid(rows=tuple(new_rows)), True


def solve_a(input: StringIO) -> int:
    grid = Grid.parse(input)
    sand_count = 0
    added_sand = True
    while added_sand:
        grid, added_sand = grid.add_sand(500, 0)
        if added_sand:
            sand_count += 1

    return sand_count


def solve_b(input: StringIO) -> int:
    grid = Grid.parse(input, add_floor=True)
    sand_count = 0
    added_sand = True
    while added_sand:
        grid, added_sand = grid.add_sand(500, 0)
        if added_sand:
            sand_count += 1
        else:
            grid.print()

    return sand_count


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
