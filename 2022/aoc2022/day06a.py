from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_06.txt"


def find_marker(input: str, number_of_chars: int) -> int:
    # Cleaned up and simplified after submitting
    for end_index in range(number_of_chars, len(input)):
        chars = input[end_index - number_of_chars:end_index]
        if len(set(chars)) == number_of_chars:
            return end_index

    raise ValueError("No match found!")


def solve(input: str) -> int:
    return find_marker(input, 4)


if __name__ == "__main__":
    print(solve(INPUT_FILE.read_text()))
