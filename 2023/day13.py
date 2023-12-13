import sys

INPUT = open(sys.argv[1]).read().strip()


def rotate90(matrix):
    rotated = []
    for i in range(len(matrix[0])):
        li = list(map(lambda x: x[i], matrix))
        li.reverse()
        rotated.append(li)

    return tuple([tuple(l) for l in rotated])


def get_vertical_mirror(pattern, smudge=0):
    for ri in range(0, len(pattern) - 1):
        before, after = pattern[: ri + 1], pattern[ri + 1 :]
        if smudge == 0:
            if all([a == b for a, b in zip(reversed(before), after)]):
                return ri + 1
        else:
            mismatches = 0
            for a, b in zip(reversed(before), after):
                for a_val, b_val in zip(a, b):
                    if a_val != b_val:
                        mismatches += 1
                if mismatches > smudge:
                    continue
            if mismatches == smudge:
                return ri + 1
    return None


def get_horizontal_mirror(pattern, smudge=0):
    rotated_pattern = rotate90(pattern)
    return get_vertical_mirror(rotated_pattern, smudge=smudge)


def part1():
    total = 0
    patterns = INPUT.split("\n\n")

    for pattern in patterns:
        pattern = tuple([tuple([c for c in line]) for line in pattern.splitlines()])

        vscore = get_vertical_mirror(pattern)
        if vscore:
            total += vscore * 100
        else:
            hscore = get_horizontal_mirror(pattern)
            if hscore:
                total += hscore

    return total


def part2():
    total = 0
    patterns = INPUT.split("\n\n")

    for pattern in patterns:
        pattern = tuple([tuple([c for c in line]) for line in pattern.splitlines()])

        vscore = get_vertical_mirror(pattern, smudge=1)
        if vscore:
            total += vscore * 100
        else:
            hscore = get_horizontal_mirror(pattern, smudge=1)
            if hscore:
                total += hscore

    return total


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
