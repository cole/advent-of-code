import pathlib
from io import StringIO

INPUT_FILE = pathlib.Path(pathlib.Path(__file__).parent.parent, "data/input_01.txt")


def calorie_counter(calories: StringIO) -> int:
    current_elf_counter = 0
    max_calories_carried = 0
    for line in calories:
        # Empty string means next elf
        if line == "\n":
            max_calories_carried = max(max_calories_carried, current_elf_counter)
            current_elf_counter = 0
        else:
            current_elf_counter += int(line.rstrip("\n"))

    return max_calories_carried


if __name__ == "__main__":
    input = StringIO(INPUT_FILE.read_text())
    print(calorie_counter(input))
