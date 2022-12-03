from io import StringIO
from aoc2022.day02a import check_strategy as check_strategy_a
from aoc2022.day02b import check_strategy as check_strategy_b

TEST_DATA = """A Y
B X
C Z"""


def test_check_strategy_a():
    input = StringIO(TEST_DATA)
    assert check_strategy_a(input) == 15


def test_check_strategy_b():
    input = StringIO(TEST_DATA)
    assert check_strategy_b(input) == 12
