import re
from io import StringIO

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_05.txt"
MOVE_REGEX = re.compile(r"move (\d+) from (\d+) to (\d+)")


def parse_initial_stacks(stack_input: str):
    lines = stack_input.split("\n")
    lines.reverse()

    stacks = []
    for _ in lines[0].split():
        stacks.append([])

    for line in lines[1:]:
        for col_number, _ in enumerate(stacks):
            index = (col_number * 3) + (col_number + 1)
            value = line[index].strip()
            if value:
                stacks[col_number].append(value)

    return stacks


def do_move(stacks, command: str):
    parsed_command = MOVE_REGEX.match(command)
    if not parsed_command:
        raise ValueError(f"Invalid command: {command}")
    num_to_move = int(parsed_command.group(1))
    start = int(parsed_command.group(2))
    end = int(parsed_command.group(3))

    start_stack = stacks[start - 1]
    end_stack = stacks[end - 1]

    move_stack = []
    for _ in range(num_to_move):
        move_stack.append(start_stack.pop())

    while move_stack:
        item = move_stack.pop()
        end_stack.append(item)


def solve(input: StringIO) -> str:
    input_val = input.getvalue()
    initial_positions, moves = input_val.split("\n\n")
    stacks = parse_initial_stacks(initial_positions)

    for move in moves.split("\n"):
        if move:
            do_move(stacks, move)

    output = "".join([stack[-1] for stack in stacks if stack])

    return output


if __name__ == "__main__":
    print(solve(StringIO(INPUT_FILE.read_text())))
