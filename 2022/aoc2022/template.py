from io import StringIO
from timeit import default_timer as timer

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_00.txt"


def solve_a(input: StringIO) -> int:
    return 0


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
