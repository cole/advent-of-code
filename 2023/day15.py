import sys

INPUT = open(sys.argv[1]).read().strip()


def hash(val):
    """
    Determine the ASCII code for the current character of the string.
    Increase the current value by the ASCII code you just determined.
    Set the current value to itself multiplied by 17.
    Set the current value to the remainder of dividing itself by 256.
    """
    curr = 0
    for char in val:
        curr += ord(char)
        curr = curr * 17
        curr = curr % 256

    return curr


def part1():
    return sum(map(hash, INPUT.split(",")))


class Box:
    def __init__(self, box_no):
        self.box_no = box_no
        self.lenses = []
        self.focals = {}

    @property
    def power(self):
        total = 0
        for i, label in enumerate(self.lenses, start=1):
            focal = self.focals[label]
            lens_power = (self.box_no + 1) * i * focal
            total += lens_power

        return total

    def remove(self, label):
        try:
            self.lenses.pop(self.lenses.index(label))
        except ValueError:
            pass
        else:
            del self.focals[label]

    def set(self, label, focal):
        try:
            idx = self.lenses.index(label)
        except ValueError:
            idx = None

        if idx is None:
            self.lenses.append(label)

        self.focals[label] = focal


def part2():
    boxes = [Box(i) for i in range(256)]
    for step in INPUT.replace("\n", "").split(","):
        op = "="
        try:
            op_idx = step.index(op)
        except ValueError:
            op = "-"
            op_idx = step.index("-")

        label = step[0:op_idx]

        box = boxes[hash(label)]
        if op == "-":
            box.remove(label)
        elif op.startswith("="):
            focal = int(step[op_idx + 1 :])
            box.set(label, focal)

    return sum([b.power for b in boxes])


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
