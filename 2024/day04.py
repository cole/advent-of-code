import re
import sys

INPUT = open(sys.argv[1]).read().strip()

split_input = INPUT.split("\n")


def char_at(x, y, offset=(-1, -1)):
    x_offset, y_offset = offset
    pos_y = y + y_offset
    pos_x = x + x_offset

    if pos_y < 0 or pos_x < 0:
        return None

    try:
        return split_input[pos_y][pos_x]
    except IndexError:
        return None


def check_diagonal(start_x, start_y, dir="bottom_left"):
    if dir == "bottom_left":
        offset = (-1, 1)
    elif dir == "bottom_right":
        offset = (1, 1)
    elif dir == "top_left":
        offset = (-1, -1)
    elif dir == "top_right":
        offset = (1, -1)
    else:
        raise ValueError(f"Invalid direction: {dir}")

    for i, expected in zip(range(0, 4), "XMAS"):
        char = char_at(start_x, start_y, offset=(offset[0] * i, offset[1] * i))
        if char != expected:
            return False

    return True


def part1():
    horizontal_count = 0
    vertical_count = 0
    diagonal_count = 0

    for line in split_input:
        horizontal_count += len(re.findall(r"XMAS", line))
        horizontal_count += len(re.findall(r"SAMX", line))

    input_height = len(split_input)
    input_width = len(split_input[0])
    for x in range(input_width):
        column = "".join([split_input[y][x] for y in range(input_height)])
        vertical_count += len(re.findall(r"XMAS", column))
        vertical_count += len(re.findall(r"SAMX", column))

    for y in range(input_height):
        for x in range(input_width):
            if check_diagonal(x, y, "bottom_left"):
                diagonal_count += 1
            if check_diagonal(x, y, "bottom_right"):
                diagonal_count += 1
            if check_diagonal(x, y, "top_left"):
                diagonal_count += 1
            if check_diagonal(x, y, "top_right"):
                diagonal_count += 1

    return horizontal_count + vertical_count + diagonal_count


def part2():
    xmas_count = 0
    for y, line in enumerate(split_input):
        for x, char in enumerate(line):
            if char != "A":
                continue

            x_chars_1 = [
                char_at(x, y, offset=(-1, -1)),
                char_at(x, y, offset=(1, 1)),
            ]
            x_chars_2 = [
                char_at(x, y, offset=(1, -1)),
                char_at(x, y, offset=(-1, 1)),
            ]
            if (x_chars_1 == ["S", "M"] or x_chars_1 == ["M", "S"]) and (
                x_chars_2 == ["S", "M"] or x_chars_2 == ["M", "S"]
            ):
                xmas_count += 1

    return xmas_count


print(part1())
print(part2())
