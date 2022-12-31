from io import StringIO
from aoc2022.day17 import solve_a, solve_b


TEST_DATA = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input, 2022) == 3068


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 0
