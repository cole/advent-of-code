import pathlib
from io import StringIO

INPUT_FILE = pathlib.Path(pathlib.Path(__file__).parent.parent, "data/input_01.txt")


def top_3_calorie_counter(calories: StringIO) -> int:
    elf_calories = []
    current_elf_counter = 0
    for line in calories:
        # Empty string means next elf
        if line == "\n":
            elf_calories.append(current_elf_counter)
            current_elf_counter = 0
        else:
            current_elf_counter += int(line.rstrip("\n"))

    elf_calories.append(current_elf_counter)

    return sum(sorted(elf_calories, reverse=True)[:3])


if __name__ == "__main__":
    input = StringIO(INPUT_FILE.read_text())
    print(top_3_calorie_counter(input))
