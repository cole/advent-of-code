"""
Initial solution was more convoluted, got stuck trying to make a bunch of shape classes
"""
from dataclasses import dataclass
from io import StringIO
from timeit import default_timer as timer

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_17.txt"

EMPTY = "."
ROCK = "#"
ACTIVE = "@"

MINUS = [[EMPTY, EMPTY, ACTIVE, ACTIVE, ACTIVE, ACTIVE, EMPTY]]
PLUS = [
    [EMPTY, EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, ACTIVE, ACTIVE, ACTIVE, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY, EMPTY],
]
# reversed
L_SHAPE = [
    [EMPTY, EMPTY, ACTIVE, ACTIVE, ACTIVE, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY],
]
LINE = [
    [EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, ACTIVE, EMPTY, EMPTY, EMPTY, EMPTY],
]
SQUARE = [
    [EMPTY, EMPTY, ACTIVE, ACTIVE, EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, ACTIVE, ACTIVE, EMPTY, EMPTY, EMPTY],
]


@dataclass
class Chamber:
    moves: str
    rows: list[list[str]]
    move_index: int = 0

    @property
    def active_rows(self):
        return [(index, row) for index, row in enumerate(self.rows) if ACTIVE in row]

    @property
    def move(self) -> str:
        return self.moves[self.move_index % len(self.moves)]

    def can_move_left(self, row: list[str]) -> bool:
        first_active_index = row.index(ACTIVE)
        if first_active_index == 0:
            return False
        elif row[first_active_index - 1] == ROCK:
            return False

        return True

    def can_move_right(self, row: list[str]) -> bool:
        if row[6] == ACTIVE:
            return False

        reversed_active_index = list(reversed(row)).index(ACTIVE)
        last_active_index = len(row) - reversed_active_index - 1
        if row[last_active_index + 1] == ROCK:
            return False

        return True

    def can_move_down(self, y_index: int, row: list[str]) -> bool:
        if y_index == 0:
            return False

        can_move_down = True

        for x_index, value in enumerate(row):
            if value != ACTIVE:
                continue

            value_below = self.rows[y_index - 1][x_index]
            if value_below == ROCK:
                can_move_down = False
                break

        return can_move_down

    def move_left(self):
        can_move_left = all([self.can_move_left(row) for _, row in self.active_rows])

        if can_move_left:
            for _, row in self.active_rows:
                active_indices = [
                    index for index, value in enumerate(row) if value == ACTIVE
                ]
                row[min(active_indices) - 1] = ACTIVE
                row[max(active_indices)] = EMPTY

    def move_right(self):
        can_move_right = all([self.can_move_right(row) for _, row in self.active_rows])

        if can_move_right:
            for _, row in self.active_rows:
                active_indices = [
                    index for index, value in enumerate(row) if value == ACTIVE
                ]
                row[max(active_indices) + 1] = ACTIVE
                row[min(active_indices)] = EMPTY

    def move_down(self) -> bool:
        can_move_down = all(
            [self.can_move_down(index, row) for index, row in self.active_rows]
        )

        if can_move_down:
            for y_index, row in self.active_rows:
                for x_index, value in enumerate(row):
                    if value == ACTIVE:
                        self.rows[y_index - 1][x_index] = ACTIVE
                        self.rows[y_index][x_index] = EMPTY

        return can_move_down

    def add_shape(self, shape: list[list[str]]):
        rows_to_add = 0
        if len(self.rows) < 3:
            rows_to_add = 3 - len(self.rows)

        for row in self.rows[-3:]:
            if not all([value == EMPTY for value in row]):
                rows_to_add += 1

        if rows_to_add:
            for _ in range(rows_to_add):
                self.rows.append([EMPTY] * 7)

        # create a copy
        for row in shape:
            self.rows.append([val for val in row])

    def freeze_shape(self):
        for y_index, row in self.active_rows:
            for x_index, value in enumerate(row):
                if value == ACTIVE:
                    self.rows[y_index][x_index] = ROCK

    def trim(self):
        remove_row_indices = []
        for reversed_index, row in enumerate(reversed(self.rows)):
            if all([value == EMPTY for value in row]):
                remove_row_indices.append(len(self.rows) - reversed_index - 1)
            else:
                break

        for index in remove_row_indices:
            del self.rows[index]

    def print(self):
        for row in reversed(self.rows):
            print(f"|{''.join(row)}|")

        print("+-------+")

    def process(self, rock_count: int):
        shape_cycle = [MINUS, PLUS, L_SHAPE, LINE, SQUARE]
        rocks_fallen = 0
        while rocks_fallen < rock_count:
            next_shape = shape_cycle[0]
            shape_cycle.append(shape_cycle.pop(0))
            self.add_shape(next_shape)

            still_moving = True
            while still_moving:
                if self.move == "<":
                    self.move_left()
                elif self.move == ">":
                    self.move_right()

                self.move_index += 1

                still_moving = self.move_down()

            self.freeze_shape()
            self.trim()
            rocks_fallen += 1


def solve_a(input: StringIO, rocks: int) -> int:
    input_pattern = input.readline().rstrip("\n")

    chamber = Chamber(input_pattern, [])

    chamber.process(rocks)
    # chamber.print()
    return len(chamber.rows)


def solve_b(input: StringIO) -> int:
    return 0


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input, 2022)
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input)
    end_b = timer()
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
