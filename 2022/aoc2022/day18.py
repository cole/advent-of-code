from io import StringIO
from timeit import default_timer as timer
from typing import NamedTuple, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_18.txt"


class Cube(NamedTuple):
    x: int
    y: int
    z: int

    @property
    def side_positions(self):
        return [
            Cube(self.x + 1, self.y, self.z),
            Cube(self.x - 1, self.y, self.z),
            Cube(self.x, self.y + 1, self.z),
            Cube(self.x, self.y - 1, self.z),
            Cube(self.x, self.y, self.z + 1),
            Cube(self.x, self.y, self.z - 1),
        ]


def solve_a(input: StringIO) -> int:
    cubes = []
    for line in input:
        x, y, z = line.split(",")
        cube = Cube(x=int(x), y=int(y), z=int(z))
        cubes.append(cube)

    sides_count = 0
    for cube in cubes:
        others = set([other_cube for other_cube in cubes if other_cube != cube])

        for side in cube.side_positions:
            if side not in others:
                sides_count += 1

    return sides_count


def find_path_to_edge(
    cubes: set[Cube],
    edges: Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int]],
    start: Cube,
):
    x_edges, y_edges, z_edges = edges

    checked = set()
    queue = [start]
    while queue:
        cube = queue.pop()
        if cube not in checked:
            checked.add(cube)

            if (
                cube.x <= x_edges[0]
                or cube.x >= x_edges[1]
                or cube.y <= y_edges[0]
                or cube.y >= y_edges[1]
                or cube.z <= z_edges[0]
                or cube.z >= z_edges[1]
            ):
                return True

            queue.extend([side for side in cube.side_positions if side not in cubes])

    return False


def solve_b(input: StringIO) -> int:
    cubes = []
    for line in input:
        x, y, z = line.split(",")
        cube = Cube(x=int(x), y=int(y), z=int(z))
        cubes.append(cube)

    cube_set = set(cubes)
    x_edges = min([cube.x for cube in cubes]), max([cube.x for cube in cubes])
    y_edges = min([cube.y for cube in cubes]), max([cube.y for cube in cubes])
    z_edges = min([cube.z for cube in cubes]), max([cube.z for cube in cubes])
    edges = (x_edges, y_edges, z_edges)

    sides_count = 0
    for cube in cubes:
        for side in cube.side_positions:
            if side not in cube_set and find_path_to_edge(cube_set, edges, side):
                sides_count += 1

    return sides_count


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
