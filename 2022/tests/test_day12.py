from io import StringIO
from aoc2022.day12 import solve_a, solve_b


TEST_DATA = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 31


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 29
