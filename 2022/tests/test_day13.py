from io import StringIO
from aoc2022.day13 import solve_a, solve_b


TEST_DATA = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 13


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 140
