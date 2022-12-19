from io import StringIO
from aoc2022.day18 import solve_a, solve_b


TEST_DATA = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 64


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 58
