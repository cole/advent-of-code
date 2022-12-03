from io import StringIO
from itertools import islice

from .inputs import DATA_DIR
from .day03a import get_priority

INPUT_FILE = DATA_DIR / "input_03.txt"


def find_common_char(lines: list[str]) -> str:
    line_1, line_2, line_3 = lines
    for char in line_1:
        if char in line_2 and char in line_3:
            return char

    raise ValueError("No common char")


def sum_badge_priorities(input: StringIO) -> int:
    priorities = 0
    while True:
        line_group = list(islice(input, 3))
        if len(line_group) == 0:
            break
        badge = find_common_char(line_group)
        priorities += get_priority(badge)

    return priorities


if __name__ == "__main__":
    print(sum_badge_priorities(INPUT_FILE.open("r")))
