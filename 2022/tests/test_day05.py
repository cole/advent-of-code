from io import StringIO
from aoc2022.day05a import solve as solve_a
from aoc2022.day05b import solve as solve_b


TEST_DATA = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == "CMZ"


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == "MCD"
