from io import StringIO
from aoc2022.day02a import check_strategy

TEST_DATA = """A Y
B X
C Z"""


def test_check_strategy():
    input = StringIO(TEST_DATA)
    assert check_strategy(input) == 15
