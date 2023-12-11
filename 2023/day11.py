import itertools
import sys

INPUT = open(sys.argv[1]).read().strip()


def find_galaxies(universe):
    vals = []
    for y, l in enumerate(universe):
        for x, c in enumerate(l):
            if c == "#":
                vals.append((x, y))

    return vals


def expand(galaxies, factor=2):
    height = max([y for _, y in galaxies])
    width = max([x for x, _ in galaxies])

    x_expansions, y_expansions = [], []
    for y_col in range(width):
        if not any([y == y_col for _, y in galaxies]):
            y_expansions.append(y_col)

    for row in range(height):
        if not any([x == row for x, _ in galaxies]):
            x_expansions.append(row)

    expanded_galaxies = []
    for x, y in galaxies:
        x_mod = len([v for v in x_expansions if v < x])
        y_mod = len([v for v in y_expansions if v < y])
        expanded_galaxies.append(
            (
                x + ((factor - 1) * x_mod),
                y + ((factor - 1) * y_mod),
            )
        )

    return expanded_galaxies


def dist(a, b) -> int:
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def part1():
    galaxies = expand(
        find_galaxies([list(line) for line in INPUT.splitlines()]), factor=2
    )

    path_lengths = 0
    for start, end in itertools.combinations(galaxies, 2):
        path_lengths += dist(start, end)

    return path_lengths


def part2():
    galaxies = expand(
        find_galaxies([list(line) for line in INPUT.splitlines()]), factor=1_000_000
    )

    path_lengths = 0
    for start, end in itertools.combinations(galaxies, 2):
        path_lengths += dist(start, end)

    return path_lengths


print(f"part 1: {part1()}")
print(f"part 2: {part2()}")


# FML, I did a bunch of work implementing astar
# def neighbours(x, y):
#     vals = []
#     if x > 0:
#         vals.append((x - 1, y))
#     if y > 0:
#         vals.append((x, y - 1))
#     try:
#         universe[y + 1][x]
#     except IndexError:
#         pass
#     else:
#         vals.append((x, y + 1))
#     try:
#         universe[y][x + 1]
#     except IndexError:
#         pass
#     else:
#         vals.append((x + 1, y))

#     return vals


# def astar_search(start, end):
#     q = queue.PriorityQueue()
#     q.put((0, start))
#     visited = {}
#     costs = {}
#     visited[start] = None
#     costs[start] = 0

#     while not q.empty():
#         _, current = q.get()

#         if current == end:
#             break

#         for next in neighbours(*current):
#             new_cost = costs[current] + 1
#             if next not in costs or new_cost < costs[next]:
#                 costs[next] = new_cost
#                 priority = new_cost + heuristic(next, end)
#                 q.put((priority, next))
#                 visited[next] = current

#     return visited, costs


# def path(visited, start, end):
#     current = end
#     path = []
#     if end not in visited:
#         return []
#     while current != start:
#         path.append(current)
#         current = visited[current]

#     path.reverse()

#     return path
