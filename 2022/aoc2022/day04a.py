from io import StringIO

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_04.txt"


def fully_contains(range1: str, range2: str) -> bool:
    min_range1, max_range1 = range1.split("-")
    min_range2, max_range2 = range2.split("-")

    if int(min_range1) >= int(min_range2) and int(max_range1) <= int(max_range2):
        return True
    elif int(min_range2) >= int(min_range1) and int(max_range2) <= int(max_range1):
        return True

    return False


def solve(input: StringIO) -> int:
    count = 0
    for line in input:
        range1, range2 = line.split(",")

        if fully_contains(range1, range2):
            count += 1

    return count


if __name__ == "__main__":
    print(solve(INPUT_FILE.open("r")))
