import pathlib
from io import StringIO

INPUT_FILE = pathlib.Path(pathlib.Path(__file__).parent.parent, "data/input_01.txt")


def calorie_counter(calories: StringIO) -> int:
    return 0


if __name__ == "__main__":
    print(calorie_counter(INPUT_FILE.read_text()))
