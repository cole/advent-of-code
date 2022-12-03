from io import StringIO
from aoc2022.day01a import max_calorie_counter
from aoc2022.day01b import top_3_calorie_counter

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


def test_max_calorie_counter():
    assert max_calorie_counter(StringIO(TEST_DATA)) == 24000


def test_top_3_calorie_counter():
    assert top_3_calorie_counter(StringIO(TEST_DATA)) == 45000
