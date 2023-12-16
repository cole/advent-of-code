import collections
import sys

INPUT = open(sys.argv[1]).read().strip()


grid = tuple([tuple([c for c in line]) for line in INPUT.splitlines()])

Point = collections.namedtuple("Point", ["x", "y"])


class Beam:
    def __init__(self, start, travelling):
        self.start = start
        self.direction = travelling

    def __str__(self):
        return f"Beam({self.start}, {self.direction})"

    def trace(self):
        x, y = self.start
        direction = self.direction
        while True:
            if y < 0:
                break
            if x < 0:
                break
            try:
                c = grid[y][x]
            except IndexError:
                break

            point = Point(x, y)
            yield point

            match (c, direction):
                case (".", "up") | ("|", "up"):
                    y = y - 1
                case (".", "down") | ("|", "down"):
                    y = y + 1
                case (".", "left") | ("-", "left"):
                    x = x - 1
                case (".", "right") | ("-", "right"):
                    x = x + 1
                case ("/", "right") | ("\\", "left"):
                    direction = "up"
                    y = y - 1
                case ("/", "left") | ("\\", "right"):
                    direction = "down"
                    y = y + 1
                case ("/", "up") | ("\\", "down"):
                    direction = "right"
                    x = x + 1
                case ("/", "down") | ("\\", "up"):
                    direction = "left"
                    x = x - 1
                case ("|", "left") | ("|", "right"):
                    yield Beam(Point(x, y - 1), "up")
                    yield Beam(Point(x, y + 1), "down")
                    break
                case ("-", "up") | ("-", "down"):
                    yield Beam(Point(x - 1, y), "left")
                    yield Beam(Point(x + 1, y), "right")
                    break
                case _:
                    raise ValueError(f"Unexpected char {c}")


def count_energized(start, direction):
    beam_q = collections.deque()
    beam_q.append(Beam(start, direction))
    traced_beams = set()
    energized = set()

    while len(beam_q):
        beam = beam_q.popleft()
        if (beam.start, beam.direction) in traced_beams:
            continue

        for p in beam.trace():
            if isinstance(p, Beam):
                beam_q.append(p)
            else:
                energized.add(p)

        traced_beams.add((beam.start, beam.direction))

    return len(energized)


def part1():
    return count_energized(Point(0, 0), "right")


def part2():
    height = len(grid)
    width = len(grid[0])

    energized = 0

    for y in range(height):
        from_left = count_energized(Point(0, y), "right")
        from_right = count_energized(Point(width - 1, y), "left")

        energized = max(energized, from_left, from_right)

    for x in range(width):
        from_top = count_energized(Point(x, 0), "down")
        from_bottom = count_energized(Point(x, height - 1), "up")

        energized = max(energized, from_top, from_bottom)

    return energized


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")
