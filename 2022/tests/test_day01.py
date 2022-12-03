from io import StringIO
from aoc2022.day01a import calorie_counter

TEST_DATA = """1000
2000
3000

4000

5000
6000

7000
8000
9000

10000"""


def test_calorie_counter():
    assert calorie_counter(StringIO(TEST_DATA)) == 24000
