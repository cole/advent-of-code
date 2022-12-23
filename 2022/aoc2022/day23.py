from dataclasses import dataclass, field
from io import StringIO
from timeit import default_timer as timer
from typing import NamedTuple, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_23.txt"


class Point(NamedTuple):
    y: int
    x: int

    @property
    def adjacent_points(self) -> list["Point"]:
        return [
            Point(self.y - 1, self.x - 1),
            Point(self.y - 1, self.x),
            Point(self.y - 1, self.x + 1),
            Point(self.y, self.x - 1),
            Point(self.y, self.x + 1),
            Point(self.y + 1, self.x - 1),
            Point(self.y + 1, self.x),
            Point(self.y + 1, self.x + 1),
        ]

    @property
    def north_points(self) -> list["Point"]:
        return [
            Point(self.y - 1, self.x - 1),
            Point(self.y - 1, self.x),
            Point(self.y - 1, self.x + 1),
        ]

    @property
    def south_points(self) -> list["Point"]:
        return [
            Point(self.y + 1, self.x - 1),
            Point(self.y + 1, self.x),
            Point(self.y + 1, self.x + 1),
        ]

    @property
    def west_points(self) -> list["Point"]:
        return [
            Point(self.y + 1, self.x - 1),
            Point(self.y, self.x - 1),
            Point(self.y - 1, self.x - 1),
        ]

    @property
    def east_points(self) -> list["Point"]:
        return [
            Point(self.y + 1, self.x + 1),
            Point(self.y, self.x + 1),
            Point(self.y - 1, self.x + 1),
        ]


@dataclass
class Elf:
    position: Point
    directional_queue: list[str] = field(default_factory=lambda: ["N", "S", "W", "E"])

    def cycle_directionaL_queue(self):
        self.directional_queue.append(self.directional_queue.pop(0))


@dataclass
class State:
    elf_positions: dict[Point, Elf] = field(default_factory=dict)
    round_proposals: dict[Point, list[Elf]] = field(default_factory=dict)

    @classmethod
    def parse(cls, input: StringIO):
        state = cls()

        for y, line in enumerate(input):
            for x, char in enumerate(line.strip()):
                if char == "#":
                    point = Point(y=y, x=x)
                    state.elf_positions[point] = Elf(point)

        return state

    @property
    def elf_count(self) -> int:
        return len(self.elf_positions)

    @property
    def bounds(self) -> Tuple[int, int, int, int]:
        min_x = min([point.x for point in self.elf_positions.keys()])
        max_x = max([point.x for point in self.elf_positions.keys()])
        min_y = min([point.y for point in self.elf_positions.keys()])
        max_y = max([point.y for point in self.elf_positions.keys()])

        return (min_x, min_y, max_x, max_y)

    def move_elf(self, start_point: Point, dest_point: Point):
        elf = self.elf_positions.pop(start_point)
        elf.position = dest_point
        self.elf_positions[dest_point] = elf

    def make_proposals(self):
        self.round_proposals = {}

        for point, elf in self.elf_positions.items():
            if any(
                [
                    adjacent_point in self.elf_positions
                    for adjacent_point in point.adjacent_points
                ]
            ):
                elf_proposal = None
                for direction in elf.directional_queue:
                    if direction == "N" and not any(
                        [
                            north_point in self.elf_positions
                            for north_point in point.north_points
                        ]
                    ):
                        elf_proposal = Point(point.y - 1, point.x)
                    elif direction == "S" and not any(
                        [
                            south_point in self.elf_positions
                            for south_point in point.south_points
                        ]
                    ):
                        elf_proposal = Point(point.y + 1, point.x)
                    elif direction == "W" and not any(
                        [
                            west_point in self.elf_positions
                            for west_point in point.west_points
                        ]
                    ):
                        elf_proposal = Point(point.y, point.x - 1)
                    elif direction == "E" and not any(
                        [
                            east_point in self.elf_positions
                            for east_point in point.east_points
                        ]
                    ):
                        elf_proposal = Point(point.y, point.x + 1)

                    if elf_proposal:
                        self.round_proposals.setdefault(elf_proposal, [])
                        self.round_proposals[elf_proposal].append(elf)
                        break

    def do_moves(self) -> int:
        move_count = 0
        for point, elves in self.round_proposals.items():
            if len(elves) == 1:
                self.move_elf(elves[0].position, point)
                move_count += 1

        for elf in self.elf_positions.values():
            elf.cycle_directionaL_queue()

        return move_count

    def draw(self):
        min_x, min_y, max_x, max_y = self.bounds

        for y in range(min_y, max_y + 1):
            line = []
            for x in range(min_x, max_x + 1):
                if Point(y, x) in self.elf_positions:
                    line.append("#")
                else:
                    line.append(".")

            print("".join(line))


def solve_a(input: StringIO) -> int:
    state = State.parse(input)

    round = 0
    # print("=== Initial state")
    # state.draw()
    # print(f"Bounds: {state.bounds}")

    while round < 10:
        state.make_proposals()
        state.do_moves()

        # print(f"=== End of Round {round + 1}")
        # state.draw()
        # print(f"Bounds: {state.bounds}")

        round += 1

    area = (state.bounds[2] + 1 - state.bounds[0]) * (
        state.bounds[3] + 1 - state.bounds[1]
    )
    return area - state.elf_count


def solve_b(input: StringIO) -> int:
    # 17s, pretty slow
    state = State.parse(input)

    round = 0

    while True:
        state.make_proposals()
        move_count = state.do_moves()

        round += 1

        if move_count == 0:
            break

    return round


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
