from io import StringIO

from .inputs import DATA_DIR

INPUT_FILE = DATA_DIR / "input_01.txt"


def max_calorie_counter(calories: StringIO) -> int:
    current_elf_counter = 0
    max_calories_carried = 0
    for line in calories:
        # Empty string means next elf
        if line == "\n":
            max_calories_carried = max(max_calories_carried, current_elf_counter)
            current_elf_counter = 0
        else:
            current_elf_counter += int(line.rstrip("\n"))

    max_calories_carried = max(max_calories_carried, current_elf_counter)

    return max_calories_carried


if __name__ == "__main__":
    print(max_calorie_counter(INPUT_FILE.open("r")))
