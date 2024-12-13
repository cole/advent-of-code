import re
import sys

INPUT = open(sys.argv[1]).read().strip()
SAMPLE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279"""


def find_presses(a, b, prize, modifier=10000000000000):
    a_x_max = (prize[0] + modifier) // a[0]
    a_y_max = (prize[1] + modifier) // a[1]
    a_max = min(a_x_max, a_y_max)
    b_x_max = (prize[0] + modifier) // b[0]
    b_y_max = (prize[1] + modifier) // b[1]
    b_max = min(b_x_max, b_y_max)

    possibles = []

    for a_presses in range(a_max + 1):
        for b_presses in range(b_max + 1):
            if (
                a_presses * a[0] + b_presses * b[0] == prize[0]
                and a_presses * a[1] + b_presses * b[1] == prize[1]
            ):
                possibles.append((a_presses, b_presses))

    return min(possibles, key=lambda x: x[0] * 3 + x[1], default=(0, 0))


def part1():
    tokens = 0
    for machine in SAMPLE.split("\n\n"):
        a = re.match(r"Button A: X\+(\d+), Y\+(\d+)", machine.split("\n")[0]).groups()
        b = re.match(r"Button B: X\+(\d+), Y\+(\d+)", machine.split("\n")[1]).groups()
        prize = re.match(r"Prize: X=(\d+), Y=(\d+)", machine.split("\n")[2]).groups()

        a_presses, b_presses = find_presses(
            (int(a[0]), int(a[1])),
            (int(b[0]), int(b[1])),
            (int(prize[0]), int(prize[1])),
        )
        tokens += (a_presses * 3) + (b_presses * 1)

    return tokens


def part2():
    pass


print(part1())
print(part2())
