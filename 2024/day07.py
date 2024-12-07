import itertools
import sys

INPUT = open(sys.argv[1]).read().strip()


parsed = {}
for line in INPUT.split("\n"):
    test_value, rest = line.split(": ")
    parsed[int(test_value)] = tuple(int(x) for x in rest.split())


class Expression:
    def __init__(self, test_value, numbers, operators=("+", "*")):
        self.test_value = test_value
        self.numbers = numbers
        self.operators = operators

    @property
    def operator_possibilities(self):
        return list(itertools.product(self.operators, repeat=len(self.numbers) - 1))

    def test(self):
        for operators in self.operator_possibilities:
            expression = []
            for i, x in enumerate(self.numbers):
                expression.append(x)
                if i < len(operators):
                    expression.append(operators[i])

            if self.evaluate(expression) == self.test_value:
                return True

        return False

    def evaluate(self, expression):
        val = 0
        start, remaining = expression[:3], expression[3:]
        first, op, second = start
        if op == "+":
            val = first + second
        elif op == "*":
            val = first * second
        elif op == "||":
            val = int(f"{first}{second}")

        while remaining:
            op = remaining.pop(0)
            second = remaining.pop(0)

            if op == "+":
                val += second
            elif op == "*":
                val *= second
            elif op == "||":
                val = int(f"{val}{second}")

        return val


def part1():
    test_values = []
    for test_value, numbers in parsed.items():
        expression = Expression(test_value, numbers)
        if expression.test():
            test_values.append(expression.test_value)

    return sum(test_values)


def part2():
    test_values = []
    for test_value, numbers in parsed.items():
        expression = Expression(test_value, numbers, operators=("*", "+", "||"))
        if expression.test():
            test_values.append(expression.test_value)

    return sum(test_values)


print(part1())
print(part2())
