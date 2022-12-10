from io import StringIO
from aoc2022.day09 import solve_a, solve_b


TEST_DATA_1 = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

TEST_DATA_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""


def test_solve_a():
    input = StringIO(TEST_DATA_1)
    assert solve_a(input) == 13


def test_solve_b1():
    input = StringIO(TEST_DATA_1)
    assert solve_b(input) == 1


def test_solve_b2():
    input = StringIO(TEST_DATA_2)
    assert solve_b(input) == 36
