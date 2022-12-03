from io import StringIO

from .inputs import DATA_DIR

INPUT_FILE = DATA_DIR / "input_03.txt"


def split_compartments(rucksack: str):
    midpoint = len(rucksack) // 2
    return rucksack[0:midpoint], rucksack[midpoint:]


def get_overlapping_item(compartment_a: str, compartment_b: str) -> str:
    for char in compartment_a:
        if char in compartment_b:
            return char

    raise ValueError("No overlap")


def get_priority(char: str) -> int:
    if char.isupper():
        # A begins at 65, so offset
        return ord(char) - 38
    else:
        # lowercase begins at 97
        return ord(char) - 96


def sum_priorities(input: StringIO) -> int:
    priorities = 0
    for line in input:
        compartment_a, compartment_b = split_compartments(line)
        item = get_overlapping_item(compartment_a, compartment_b)
        item_priority = get_priority(item)
        priorities += item_priority

    return priorities


if __name__ == "__main__":
    print(sum_priorities(INPUT_FILE.open("r")))
