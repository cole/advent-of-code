input_data = """..."""


def line_value(line):
    pos = 0

    while True:
        window = line[pos:]
        match window:
            case word if word.startswith('one'):
                return 1
            case word if word.startswith('two'):
                return 2
            case word if word.startswith('three'):
                return 3
            case word if word.startswith('four'):
                return 4
            case word if word.startswith('five'):
                return 5
            case word if word.startswith('six'):
                return 6
            case word if word.startswith('seven'):
                return 7
            case word if word.startswith('eight'):
                return 8
            case word if word.startswith('nine'):
                return 9
            case _:
                try:
                    value = int(window[0])
                except ValueError:
                    pass
                else:
                    return value
            
        pos += 1



def line_value_reverse(line):
    pos = len(line)

    while True:
        window = line[0:pos]
        match window:
            case word if word.endswith('one'):
                return 1
            case word if word.endswith('two'):
                return 2
            case word if word.endswith('three'):
                return 3
            case word if word.endswith('four'):
                return 4
            case word if word.endswith('five'):
                return 5
            case word if word.endswith('six'):
                return 6
            case word if word.endswith('seven'):
                return 7
            case word if word.endswith('eight'):
                return 8
            case word if word.endswith('nine'):
                return 9
            case _:
                try:
                    value = int(window[-1])
                except ValueError:
                    pass
                else:
                    return value
            
        pos -= 1


print(sum([
    int(f"{line_value(line)}{line_value_reverse(line)}") for line in input_data.splitlines()
]))