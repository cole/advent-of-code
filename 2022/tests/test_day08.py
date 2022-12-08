from io import StringIO
from aoc2022.day08 import solve_a, solve_b


TEST_DATA = """30373
25512
65332
33549
35390"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 21


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 8
