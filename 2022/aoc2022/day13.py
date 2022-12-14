import functools
from io import StringIO
from timeit import default_timer as timer

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_13.txt"


def compare(a: list, b: list) -> bool:
    for index in range(0, max(len(a), len(b))):
        try:
            left = a[index]
        except IndexError:
            return 1

        try:
            right = b[index]
        except IndexError:
            return -1

        if isinstance(left, int) and isinstance(right, int):
            if left < right:
                return 1
            elif left > right:
                return -1
            else:
                continue
        elif isinstance(left, list) and isinstance(right, list):
            list_comparison = compare(left, right)
            if list_comparison != 0:
                return list_comparison
            else:
                continue
        elif isinstance(left, int) and isinstance(right, list):
            return compare([left], right)
        elif isinstance(right, int) and isinstance(left, list):
            return compare(left, [right])

    return 0


def iter_packets(input: StringIO):
    packet_a, packet_b = None, None
    for line in input:
        line = line.rstrip("\n")
        if line and packet_a is not None:
            packet_b = eval(line.rstrip("\n"))
        elif line:
            packet_a = eval(line.rstrip("\n"))
        else:
            yield packet_a, packet_b
            packet_a, packet_b = None, None

    if packet_a and packet_b:
        yield packet_a, packet_b


def solve_a(input: StringIO) -> int:
    right_order_indices = []
    for index, packets in enumerate(iter_packets(input), 1):
        packet_a, packet_b = packets
        is_right_order = compare(packet_a, packet_b)
        if is_right_order == 0:
            raise ValueError(f"error comparing {packet_a}, {packet_b}")
        elif is_right_order > 0:
            right_order_indices.append(index)

    return sum(right_order_indices)


def solve_b(input: StringIO) -> int:
    divider_1 = [[2]]
    divider_2 = [[6]]
    all_packets = []
    for packet_a, packet_b in iter_packets(input):
        all_packets.append(packet_a)
        all_packets.append(packet_b)

    all_packets.extend([divider_1.copy(), divider_2.copy()])
    all_packets.sort(key=functools.cmp_to_key(compare), reverse=True)

    return (all_packets.index(divider_1) + 1) * (all_packets.index(divider_2) + 1)


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
