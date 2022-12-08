from io import StringIO
from timeit import default_timer as timer
from typing import Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_08.txt"


def parse_grid(input: StringIO) -> Tuple[Tuple[int, ...]]:
    rows = []
    for line in input:
        row = tuple([int(x) for x in line.rstrip('\n')])
        rows.append(row)

    return tuple(rows)


def get_visibility(grid, x_index, y_index) -> bool:
    x_index_max = len(grid[0]) - 1
    y_index_max = len(grid) - 1
    x = grid[y_index][x_index]

    if x_index == 0 or x_index == x_index_max:
        return True
    if y_index == 0 or y_index == y_index_max:
        return True

    x1_visible, x2_visible, y1_visible, y2_visible = True, True, True, True

    for x1_index in range(0, x_index):
        if grid[y_index][x1_index] >= x:
            x1_visible = False
            break

    for x2_index in range(x_index + 1, x_index_max + 1):
        if grid[y_index][x2_index] >= x:
            x2_visible = False
            break

    for y1_index in range(0, y_index):
        if grid[y1_index][x_index] >= x:
            y1_visible = False
            break

    for y2_index in range(y_index + 1, y_index_max + 1):
        if grid[y2_index][x_index] >= x:
            y2_visible = False
            break

    return x1_visible or x2_visible or y1_visible or y2_visible


def solve_a(input: StringIO) -> int:
    grid = parse_grid(input)
    visible_count = 0

    for y_index, row in enumerate(grid, 0):
        for x_index, _ in enumerate(row, 0):
            is_visible = get_visibility(grid, x_index, y_index)
            if is_visible:
                visible_count += 1

    return visible_count


def get_scenic_score(grid, x_index, y_index) -> int:
    x_index_max = len(grid[0]) - 1
    y_index_max = len(grid) - 1

    if x_index == 0 or x_index == x_index_max:
        return 0
    if y_index == 0 or y_index == y_index_max:
        return 0

    x_value = grid[y_index][x_index]
    x1_distance, x2_distance, y1_distance, y2_distance = 0, 0, 0, 0

    for x1_index in reversed(range(0, x_index)):
        x1_distance += 1
        if grid[y_index][x1_index] >= x_value:
            break

    for x2_index in range(x_index + 1, x_index_max + 1):
        x2_distance += 1
        if grid[y_index][x2_index] >= x_value:
            break

    for y1_index in reversed(range(0, y_index)):
        y1_distance += 1
        if grid[y1_index][x_index] >= x_value:
            break

    for y2_index in range(y_index + 1, y_index_max + 1):
        y2_distance += 1
        if grid[y2_index][x_index] >= x_value:
            break

    return x1_distance * x2_distance * y1_distance * y2_distance


def solve_b(input: StringIO) -> int:
    grid = parse_grid(input)
    max_scenic_score = 0

    for y_index, row in enumerate(grid, 0):
        for x_index, _ in enumerate(row, 0):
            tree_score = get_scenic_score(grid, x_index, y_index)
            max_scenic_score = max(tree_score, max_scenic_score)

    return max_scenic_score


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
