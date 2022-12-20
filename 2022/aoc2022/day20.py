from io import StringIO
from timeit import default_timer as timer
from typing import NamedTuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_20.txt"


class Number(NamedTuple):
    """
    Cheat to allow us to find the index of the number in a list, despite
    the presence of duplicate values.
    """
    index: int
    value: int


def mix(numbers: list[Number], initial_order: list[Number]):
    """
    Update our list of numbers in place, based on the initial list.
    """
    for number in initial_order:
        index = numbers.index(number)
        numbers.pop(index)
        numbers.insert((index + number.value) % len(numbers), number)


def solve_a(input: StringIO) -> int:
    numbers = []
    initial_zero_index = None
    for index, line in enumerate(input):
        value = int(line.rstrip())
        if value == 0:
            initial_zero_index = index
        numbers.append(Number(index=index, value=value))

    initial_order = [Number(index=num.index, value=num.value) for num in numbers]
    mix(numbers, initial_order)
    zero_index = numbers.index(Number(index=initial_zero_index, value=0))
    coordinates = (
        numbers[(zero_index + 1000) % len(numbers)],
        numbers[(zero_index + 2000) % len(numbers)],
        numbers[(zero_index + 3000) % len(numbers)],
    )
    return sum([num.value for num in coordinates])


def solve_b(input: StringIO) -> int:
    modifier = 811589153
    numbers = []
    initial_zero_index = None
    for index, line in enumerate(input):
        value = int(line.rstrip())
        if value == 0:
            initial_zero_index = index
        numbers.append(Number(index=index, value=value * modifier))

    initial_order = [Number(index=num.index, value=num.value) for num in numbers]

    for _ in range(10):
        mix(numbers, initial_order)
    zero_index = numbers.index(Number(index=initial_zero_index, value=0))
    coordinates = (
        numbers[(zero_index + 1000) % len(numbers)],
        numbers[(zero_index + 2000) % len(numbers)],
        numbers[(zero_index + 3000) % len(numbers)],
    )
    return sum([num.value for num in coordinates])


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
