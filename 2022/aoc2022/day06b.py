from .inputs import DATA_DIR
from .day06a import find_marker


INPUT_FILE = DATA_DIR / "input_06.txt"


def solve(input: str) -> int:
    return find_marker(input, 14)


if __name__ == "__main__":
    print(solve(INPUT_FILE.read_text()))
