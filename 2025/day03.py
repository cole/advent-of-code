import sys

INPUT = open(sys.argv[1]).read().strip()


def get_joltage(bank, digits=12):
    joltage_digits = []
    start = 0
    for digit in range(digits):
        max_value = -1
        max_value_index = 0

        bank_window = bank[start : len(bank) - (digits - digit - 1)]
        for index, value in enumerate(bank_window):
            if int(value) > max_value:
                max_value = int(value)
                max_value_index = index

        start = start + max_value_index + 1
        joltage_digits.append(str(max_value))

    joltage = int("".join(joltage_digits))

    # print(f"bank: {bank} digits: {joltage_digits} joltage: {joltage}")

    return joltage


def part1():
    total_joltage = 0

    for bank in INPUT.split("\n"):
        if not bank:
            continue
        total_joltage += get_joltage(bank, digits=2)

    return total_joltage


def part2():
    total_joltage = 0

    for bank in INPUT.split("\n"):
        if not bank:
            continue
        total_joltage += get_joltage(bank, digits=12)

    return total_joltage


print(part1())
print(part2())
