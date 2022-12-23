import operator
from dataclasses import dataclass
from io import StringIO
from timeit import default_timer as timer
from typing import Callable

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_21.txt"


monkeys = {}


@dataclass
class Monkey:
    value: int | None
    left_monkey_name: str | None
    right_monkey_name: str | None
    operation: str | None

    @property
    def left_monkey(self):
        if self.left_monkey_name is None:
            return None

        return monkeys[self.left_monkey_name]

    @property
    def right_monkey(self):
        if self.right_monkey_name is None:
            return None

        return monkeys[self.right_monkey_name]

    @property
    def operation_func(self) -> Callable:
        match self.operation:
            case "+":
                return operator.add
            case "-":
                return operator.sub
            case "*":
                return operator.mul
            case "/":
                return operator.floordiv
            case "=":
                return operator.eq
            case _:
                raise ValueError(f"Unknown operation: {self.operation}")

    def resolve(self):
        if self.value is not None:
            return self.value

        return self.operation_func(
            self.left_monkey.resolve(), self.right_monkey.resolve()
        )

    def resolve_operations_chain(self):
        if self.value is not None:
            return [self.value]

        return (
            self.left_monkey.resolve_operations_chain()
            + [self.operation]
            + self.right_monkey.resolve_operations_chain()
        )


def converge_on(
    number_monkey: str,
    equality_monkey: str,
    start: int = 0,
    max: int = 100_000_000_000_000,
) -> int:
    target = monkeys[equality_monkey].right_monkey.resolve()

    step_size = ((max - start) // 1000) or 1
    previous_step, previous_left_val = start, None
    for i in range(start, max, step_size):
        monkeys[number_monkey].value = i
        left_val = monkeys[equality_monkey].left_monkey.resolve()

        if left_val == target:
            return i

        if previous_left_val:
            if (
                previous_left_val < target < left_val
                or previous_left_val > target > left_val
            ):
                return converge_on(number_monkey, equality_monkey, previous_step, i)

        previous_step = i
        previous_left_val = left_val


def solve_a(input: StringIO, monkey: str) -> int:
    for line in input:
        match line.rstrip().split():
            case [monkey_name, value]:
                monkeys[monkey_name.rstrip(":")] = Monkey(int(value), None, None, None)
            case [monkey_name, left_monkey_name, operation, right_monkey_name]:
                monkeys[monkey_name.rstrip(":")] = Monkey(
                    None, left_monkey_name, right_monkey_name, operation
                )

    return monkeys[monkey].resolve()


def solve_b(input: StringIO, equality_monkey: str, number_monkey: str) -> int:
    for line in input:
        match line.rstrip().split():
            case [monkey_name, value]:
                monkeys[monkey_name.rstrip(":")] = Monkey(int(value), None, None, None)
            case [monkey_name, left_monkey_name, operation, right_monkey_name]:
                if monkey_name == f"{equality_monkey}:":
                    monkeys[monkey_name.rstrip(":")] = Monkey(
                        None, left_monkey_name, right_monkey_name, "="
                    )
                else:
                    monkeys[monkey_name.rstrip(":")] = Monkey(
                        None, left_monkey_name, right_monkey_name, operation
                    )

    return converge_on(number_monkey, equality_monkey)


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input, "root")
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input, "root", "humn")
    end_b = timer()
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
