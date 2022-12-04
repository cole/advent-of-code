from io import StringIO

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_04.txt"


def overlaps(range1: str, range2: str) -> bool:
    min_range1, max_range1 = range1.split("-")
    min_range2, max_range2 = range2.split("-")

    if int(max_range1) >= int(max_range2):
        upper_range = int(min_range1), int(max_range1)
        lower_range = int(min_range2), int(max_range2)
    else:
        upper_range = int(min_range2), int(max_range2)
        lower_range = int(min_range1), int(max_range1)

    if lower_range[1] >= upper_range[0]:
        return True

    return False


def solve(input: StringIO) -> int:
    count = 0
    for line in input:
        range1, range2 = line.split(",")

        if overlaps(range1, range2):
            print(range1, range2, "here")
            count += 1

    return count


if __name__ == "__main__":
    print(solve(INPUT_FILE.open("r")))
