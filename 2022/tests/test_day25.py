from io import StringIO

import pytest

from aoc2022.day25 import decimal_to_snafu, snafu_to_decimal, solve_a, solve_b


TEST_DATA = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""


@pytest.mark.parametrize(
    "decimal, snafu",
    [
        (1, "1"),
        (2, "2"),
        (3, "1="),
        (4, "1-"),
        (5, "10"),
        (6, "11"),
        (9, "2-"),
        (20, "1-0"),
        (2022, "1=11-2"),
        (12345, "1-0---0"),
        (314159265, "1121-1110-1=0"),
    ],
)
def test_conversions(decimal: int, snafu: str):
    assert snafu_to_decimal(snafu) == decimal
    assert decimal_to_snafu(decimal) == snafu


def test_solve_a():
    input = StringIO(TEST_DATA)
    assert solve_a(input) == "2=-1=0"


def test_solve_b():
    input = StringIO(TEST_DATA)
    assert solve_b(input) == 0
