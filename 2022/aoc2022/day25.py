from io import StringIO
from timeit import default_timer as timer

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_25.txt"


SNAFU_DIGIT_CONVERSIONS = {
    "2": 2,
    "1": 1,
    "0": 0,
    "-": -1,
    "=": -2,
}
DECIMAL_DIGIT_CONVERSIONS = {
    value: key for key, value in SNAFU_DIGIT_CONVERSIONS.items()
}


def snafu_to_decimal(snafu: str) -> int:
    total = 0

    for position, digit in enumerate(reversed(snafu)):
        if position == 0:
            total += SNAFU_DIGIT_CONVERSIONS[digit]
        else:
            column = 5**position
            total += SNAFU_DIGIT_CONVERSIONS[digit] * column

    return total


def decimal_to_snafu(decimal: int) -> str:
    snafu = ""

    while decimal != 0:
        remainder = decimal % 5
        decimal = decimal // 5
        if remainder == 4:
            digit = DECIMAL_DIGIT_CONVERSIONS[-1]
            decimal += 1
        elif remainder == 3:
            digit = DECIMAL_DIGIT_CONVERSIONS[-2]
            decimal += 1
        else:
            digit = DECIMAL_DIGIT_CONVERSIONS[remainder]

        snafu = digit + snafu

    return snafu


def solve_a(input: StringIO) -> str:
    total = 0
    for line in input:
        line_value = snafu_to_decimal(line.strip())
        total += line_value

    return decimal_to_snafu(total)


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
