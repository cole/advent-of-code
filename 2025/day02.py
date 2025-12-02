import sys

INPUT = open(sys.argv[1]).read().strip()


def is_repeated_twice(id):
    str_id = str(id)
    return (
        len(str_id) % 2 == 0
        and str_id[0 : len(str_id) // 2] == str_id[len(str_id) // 2 :]
    )


def chunk(str, length):
    return (str[0 + i : length + i] for i in range(0, len(str), length))


def is_repeated_at_least_twice(id):
    str_id = str(id)
    for pos in range(1, len(str_id)):
        if pos > len(str_id) / 2:
            return False

        repeats = chunk(str_id, pos)
        if len(set(repeats)) == 1:
            return True

    return False


def part1():
    invalid = 0
    for id_range in INPUT.split(","):
        range_parts = id_range.split("-", maxsplit=1)
        start = int(range_parts[0])
        end = int(range_parts[1])

        for id in range(start, end + 1):
            if is_repeated_twice(id):
                invalid += id

    return invalid


def part2():
    invalid = 0
    for id_range in INPUT.split(","):
        range_parts = id_range.split("-", maxsplit=1)
        start = int(range_parts[0])
        end = int(range_parts[1])

        for id in range(start, end + 1):
            if is_repeated_at_least_twice(id):
                invalid += id

    return invalid


print(part1())
print(part2())
