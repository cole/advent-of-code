from io import StringIO
from aoc2022.day22 import solve_a, solve_b


TEST_DATA = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == 6032


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 0
