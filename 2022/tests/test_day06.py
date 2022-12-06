from aoc2022.day06a import solve as solve_a
from aoc2022.day06b import solve as solve_b


TEST_DATA_A_1 = "mjqjpqmgbljsphdztnvjfqwrcgsmlb"
TEST_DATA_A_4 = "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"
TEST_DATA_B_1 = "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"


def test_solve_a_1():
    assert solve_a(TEST_DATA_A_1) == 7


def test_solve_a_2():
    assert solve_a(TEST_DATA_A_4) == 11


def test_solve_b():
    assert solve_b(TEST_DATA_B_1) == 29
