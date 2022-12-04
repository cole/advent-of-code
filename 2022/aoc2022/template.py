from io import StringIO

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_00.txt"


def solve(input: StringIO) -> int:
    return 0


if __name__ == "__main__":
    print(solve(INPUT_FILE.open("r")))
