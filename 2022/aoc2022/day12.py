from io import StringIO
from timeit import default_timer as timer
from typing import Sequence, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_12.txt"

Grid = Tuple[Tuple[int, ...]]
Coordinate = Tuple[int, int]


def parse_grid(input: StringIO) -> Tuple[Tuple[int, ...]]:
    grid = []

    start = None
    target = None

    row_index = 0
    for line in input:
        row = []
        col_index = 0
        for char in line.rstrip("\n"):
            if char == "S":
                start = (row_index, col_index)
                row.append(1)
            elif char == "E":
                target = (row_index, col_index)
                row.append(26)
            else:
                row.append(ord(char) - 96)

            col_index += 1

        grid.append(row)
        row_index += 1

    grid = tuple([tuple(row) for row in grid])

    return grid, start, target


def mark_points(grid: Grid, start: Coordinate, target: Coordinate) -> Grid:
    """
    Lee's algorithm, apparently? I had to look it up.
    """
    marks_grid = [[None for r in row] for row in grid]
    marks_grid[start[0]][start[1]] = 0

    mark_queue = [start]
    pos = start
    mark_value = 0
    while mark_queue:
        mark_value += 1

        next_queue = []

        for pos in mark_queue:
            current_elevation = grid[pos[0]][pos[1]]
            for y_mod, x_mod in ((-1, 0), (0, -1), (0, +1), (+1, 0)):
                y_index = pos[0] + y_mod
                x_index = pos[1] + x_mod
                if y_index < 0 or x_index < 0:
                    continue

                try:
                    elevation = grid[y_index][x_index]
                except IndexError:
                    continue

                if elevation <= current_elevation + 1:
                    marked = marks_grid[y_index][x_index]
                    if not marked:
                        marks_grid[y_index][x_index] = mark_value
                        next_queue.append((y_index, x_index))

        mark_queue = next_queue

    return tuple([tuple(row) for row in marks_grid])


def print_path(
    grid: Grid,
    start: Coordinate,
    target: Coordinate,
    path: Sequence[Coordinate],
) -> None:
    used_moves_grid = [["." for r in row] for row in grid]
    used_moves_grid[start[0]][start[1]] = "S"
    used_moves_grid[target[0]][target[1]] = "E"

    last_move = start

    for move in path:
        if move[0] > last_move[0]:
            used_moves_grid[last_move[0]][last_move[1]] = "v"
        elif move[0] < last_move[0]:
            used_moves_grid[last_move[0]][last_move[1]] = "^"
        elif move[1] > last_move[1]:
            used_moves_grid[last_move[0]][last_move[1]] = ">"
        elif move[1] < last_move[1]:
            used_moves_grid[last_move[0]][last_move[1]] = "<"

        last_move = move

    print(f"Path moves: {len(path)}")
    for row in used_moves_grid:
        print("".join(row))


def solve_a(input: StringIO) -> int:
    grid, start, target = parse_grid(input)
    marked_grid = mark_points(grid, start, target)

    return marked_grid[target[0]][target[1]]


def solve_b(input: StringIO) -> int:
    grid, _, target = parse_grid(input)

    starts = []
    for y_index, row in enumerate(grid):
        for x_index, elevation in enumerate(row):
            if elevation == 1:
                starts.append((y_index, x_index))

    path_lengths = []
    for start in starts:
        marked_grid = mark_points(grid, start, target)
        path_lengths.append(marked_grid[target[0]][target[1]])

    return min([length for length in path_lengths if length])


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
