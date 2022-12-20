from io import StringIO
from aoc2022.day20 import solve_a, solve_b


TEST_DATA = """1
2
-3
3
-2
0
4"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 3


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 1623178306
