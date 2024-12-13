import collections
import sys
from typing import NamedTuple

INPUT = open(sys.argv[1]).read().strip()


def part1():
    stones = [int(x) for x in INPUT.split()]
    for i in range(25):
        if i < 6:
            print(stones)

        updated = []
        for stone in stones:
            if stone == 0:
                updated.append(1)
            elif len(str(stone)) % 2 == 0:
                first, second = (
                    int(str(stone)[: len(str(stone)) // 2]),
                    int(str(stone)[len(str(stone)) // 2 :]),
                )
                updated.extend([first, second])
            else:
                updated.append(stone * 2024)

        stones = updated

    return len(stones)


Stone = NamedTuple("Stone", [("value", int), ("count", int)])


def blink(stone, rest=None, max_count=75):
    if rest is None:
        rest = []

    if stone.count == max_count:
        # print(f"Max count reached: {stone} {rest}")
        return stone, rest

    if stone.value == 0:
        next_stone = Stone(1, stone.count + 1)
    elif len(str(stone.value)) % 2 == 0:
        first, second = (
            int(str(stone.value)[: len(str(stone.value)) // 2]),
            int(str(stone.value)[len(str(stone.value)) // 2 :]),
        )
        next_stone = Stone(first, stone.count + 1)
        rest.append(Stone(second, stone.count + 1))
    else:
        next_stone = Stone(stone.value * 2024, stone.count + 1)

    return blink(next_stone, rest, max_count=max_count)


def part2(input_data):
    total = 0
    for x in input_data.split():
        queue = collections.deque([Stone(int(x), 0)])
        while len(queue) > 0:
            stone = queue.popleft()
            stone, rest = blink(stone, rest=[])
            total += 1
            queue.extend(rest)

            if total % 1_000_000 == 0:
                print(total)

        print(f"{x=}, {total=}")

    return total


if __name__ == "__main__":
    print(part1())
    print(part2(INPUT))
