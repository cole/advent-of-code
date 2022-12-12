import functools
from collections import deque
from io import StringIO
from math import prod
from operator import add, mul
from timeit import default_timer as timer
from typing import Callable, Dict, List

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_11.txt"


class Monkey:
    def __init__(
        self,
        starting_items: List[int],
        operation: str,
        test: str,
        true_index: int,
        false_index: int,
    ) -> None:
        self.items = deque(starting_items)
        self.operation_func = self._parse_operation(operation)
        self.divisor = self._parse_test(test)
        self.test_func = lambda v: v % self.divisor == 0
        self.true_index = true_index
        self.false_index = false_index
        self.inspect_count = 0

    @classmethod
    def parse_monkeys(cls, input: StringIO) -> List["Monkey"]:
        monkeys = []
        starting_items, operation, test, true_index, false_index = (
            None,
            None,
            None,
            None,
            None,
        )

        for line in input:
            match line.strip().split():
                case ["Monkey", index_str]:
                    index = int(index_str.rstrip(":"))
                    if index > 0:
                        monkeys.append(
                            cls(
                                starting_items, operation, test, true_index, false_index
                            )
                        )
                    # Start a new monkey
                    starting_items, operation, test, true_index, false_index = (
                        None,
                        None,
                        None,
                        None,
                        None,
                    )
                case ["Starting", "items:", *items]:
                    starting_items = [int(item.rstrip(",")) for item in items]
                case ["Operation:", *operation]:
                    operation = " ".join(operation)
                case ["Test:", *test_args]:
                    test = " ".join(test_args)
                case ["If", "true:", "throw", "to", "monkey", true_monkey]:
                    true_index = int(true_monkey)
                case ["If", "false:", "throw", "to", "monkey", true_monkey]:
                    false_index = int(true_monkey)
                case []:
                    pass
                case _:
                    raise ValueError(f"Unable to parse line: '{line}'")
            # Add the last monkey
        monkeys.append(cls(starting_items, operation, test, true_index, false_index))

        return monkeys

    def _parse_operation(self, operation: str):
        match operation.split():
            case ["new", "=", "old", "+", value_str]:
                op = add
            case ["new", "=", "old", "*", value_str]:
                op = mul
            case _:
                raise ValueError(f"Unknown operator '{operation}'")

        if value_str == "old":
            return lambda v: op(v, v)

        return functools.partial(op, int(value_str))

    def _parse_test(self, test: str):
        match test.split():
            case ["divisible", "by", value_str]:
                return int(value_str)
            case _:
                raise ValueError(f"Unknown test '{test}'")

    def catch(self, item: int):
        self.items.append(item)

    def take_turn(self, monkeys: List["Monkey"], divide_by_three: bool = False):
        while self.items:
            item = self.items.popleft()
            worry_level = self.operation_func(item)
            if divide_by_three:
                # Always divide by 3
                worry_level = worry_level // 3
            # simplify by dividing by the product of all monkey divisors
            divisors = [monkey.divisor for monkey in monkeys]
            worry_level = worry_level % prod(divisors)
            test_result = self.test_func(worry_level)
            index = self.true_index if test_result else self.false_index
            yield index, worry_level

            self.inspect_count += 1


def solve_a(input: StringIO) -> int:
    monkeys = Monkey.parse_monkeys(input)

    rounds = 20
    for round_num in range(rounds):
        for monkey in monkeys:
            for catch_index, thrown_item in monkey.take_turn(
                monkeys, divide_by_three=True
            ):
                monkeys[catch_index].catch(thrown_item)

        # print(f"Round: {round_num}")
        # for index, monkey in enumerate(monkeys):
        #     print(f"Monkey {index}: {list(monkey.items)}")
        # print("\n")

    inspect_counts = [
        monkey.inspect_count
        for monkey in sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)
    ]

    return mul(*inspect_counts[:2])


def solve_b(input: StringIO) -> int:
    monkeys = Monkey.parse_monkeys(input)

    rounds = 10000
    for round_num in range(rounds):
        for monkey in monkeys:
            for catch_index, thrown_item in monkey.take_turn(
                monkeys, divide_by_three=False
            ):
                monkeys[catch_index].catch(thrown_item)

        # print(f"Round: {round_num}")
        # for index, monkey in enumerate(monkeys):
        #     print(f"Monkey {index}: {list(monkey.items)}")
        # print("\n")

    inspect_counts = [
        monkey.inspect_count
        for monkey in sorted(monkeys, key=lambda m: m.inspect_count, reverse=True)
    ]

    return mul(*inspect_counts[:2])


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input)
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input)
    end_b = timer()
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
