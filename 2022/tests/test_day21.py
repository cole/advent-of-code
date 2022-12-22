from io import StringIO
from aoc2022.day21 import solve_a, solve_b


TEST_DATA = """root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32"""


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input, "root") == 152


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input, "root", "humn") == 301
