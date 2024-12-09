import array
import sys

INPUT = open(sys.argv[1]).read().strip()


FREE = -1


def parse(input):
    expanded = array.array("i")
    file_id = 0
    is_file = True
    for char in input:
        block_length = int(char)
        if is_file:
            value = file_id
        else:
            value = FREE
        expanded.extend([value] * block_length)

        if is_file:
            file_id += 1
        is_file = not is_file

    return expanded


def compress_fragmented(expanded):
    while True:
        try:
            first_free = expanded.index(FREE)
        except ValueError:
            break

        last_value = expanded.pop()
        if last_value != FREE:
            expanded[first_free] = last_value

    return expanded


def checksum(expanded):
    return sum([pos * value for pos, value in enumerate(expanded) if value != FREE])


def first_free(expanded, length, limit=None):
    for i, _ in enumerate(expanded):
        if limit is not None and i + length > limit:
            break
        if all([expanded[j] == FREE for j in range(i, i + length)]):
            return i
    return None


def reverse_files(expanded):
    current_value = None
    current_length = 0

    processed = set()

    for val in reversed(expanded):
        if val != FREE and val in processed:
            continue

        if current_value is None:
            if val != FREE:
                current_value = val
                current_length = 1
        elif val != current_value:
            yield current_value, current_length, expanded.index(current_value)
            processed.add(current_value)
            if val == FREE:
                current_value = None
                current_length = 0
            else:
                current_value = val
                current_length = 1
        elif val == current_value:
            current_length += 1

    yield current_value, current_length, expanded.index(current_value)


def compress_files(expanded):
    processed = 0
    for file_id, file_length, file_start_index in reverse_files(expanded):
        if processed % 100 == 0:
            print(
                f"Processed {processed} files, current: {file_id} at {file_start_index}"
            )
        if file_length == 0:
            continue

        try:
            first_free_index = first_free(expanded, file_length, limit=file_start_index)
        except IndexError:
            first_free_index = None

        if first_free_index is None:
            continue

        for i in range(file_length):
            expanded[first_free_index + i] = file_id
            expanded[file_start_index + i] = FREE

        processed += 1
    return expanded


def part1():
    expanded = parse(INPUT)
    compressed = compress_fragmented(expanded)
    return checksum(compressed)


def part2():
    expanded = parse(INPUT)
    compressed = compress_files(expanded)
    return checksum(compressed)


print(part1())
print(part2())
