from io import StringIO
from aoc2022.day03a import sum_priorities
from aoc2022.day03b import sum_badge_priorities

TEST_DATA = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""


def test_sum_priorities():
    input = StringIO(TEST_DATA)
    assert sum_priorities(input) == 157



def test_sum_badge_priorities():
    input = StringIO(TEST_DATA)
    assert sum_badge_priorities(input) == 70
