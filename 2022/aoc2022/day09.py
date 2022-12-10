from io import StringIO
from timeit import default_timer as timer
from typing import NamedTuple, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_09.txt"


class Coordinate(NamedTuple):
    x: int
    y: int

    def move(self, direction: str) -> "Coordinate":
        if direction == "U":
            return Coordinate(self.x, self.y - 1)
        elif direction == "D":
            return Coordinate(self.x, self.y + 1)
        elif direction == "L":
            return Coordinate(self.x - 1, self.y)
        elif direction == "R":
            return Coordinate(self.x + 1, self.y)

        raise ValueError("Invalid direction")

    def __str__(self):
        return f"{self.x}, {self.y}"


def move(rope: Tuple[Coordinate, ...], direction: str) -> Tuple[Coordinate, ...]:
    new_rope = []

    leader = None
    for index, knot in enumerate(rope):
        if index == 0:
            new_pos = knot.move(direction)
        # Touching
        elif (leader.x - 1 <= knot.x <= leader.x + 1) and (
            leader.y - 1 <= knot.y <= leader.y + 1
        ):
            new_pos = knot
        # Straight moves
        elif knot.x < leader.x and knot.y == leader.y:
            new_pos = knot.move("R")
        elif knot.x > leader.x and knot.y == leader.y:
            new_pos = knot.move("L")
        elif knot.x == leader.x and knot.y > leader.y:
            new_pos = knot.move("U")
        elif knot.x == leader.x and knot.y < leader.y:
            new_pos = knot.move("D")
        # Diagonals
        elif knot.x != leader.x and knot.y != leader.y:
            if knot.x > leader.x:
                new_pos = knot.move("L")
            else:
                new_pos = knot.move("R")

            if knot.y > leader.y:
                new_pos = new_pos.move("U")
            else:
                new_pos = new_pos.move("D")

        new_rope.append(new_pos)
        leader = new_pos

    return tuple(new_rope)


def solve_a(input: StringIO) -> int:
    head = Coordinate(0, 0)
    tail = Coordinate(0, 0)
    visited = set()

    for line in input:
        direction, raw_count = line.split()
        count = int(raw_count.strip())
        for _ in range(count):
            head, tail = move((head, tail), direction.upper().strip())
            visited.add(tail)

    return len(visited)


def solve_b(input: StringIO) -> int:
    rope = tuple([Coordinate(0, 0) for _ in range(10)])
    visited = set()

    for line in input:
        direction, raw_count = line.split()
        count = int(raw_count.strip())
        for _ in range(count):
            rope = move(rope, direction.upper().strip())
            visited.add(rope[-1])

    return len(visited)


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input)
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input)
    end_b = timer()
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
