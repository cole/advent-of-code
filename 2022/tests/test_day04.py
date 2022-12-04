from io import StringIO
from aoc2022.day04a import solve as solve_a
from aoc2022.day04b import solve as solve_b


TEST_DATA = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 2


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 4
