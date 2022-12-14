from io import StringIO
from aoc2022.day14 import solve_a, solve_b


TEST_DATA = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 24


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 93
