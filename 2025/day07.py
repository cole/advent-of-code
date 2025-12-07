import sys
from collections import defaultdict, deque

INPUT = open(sys.argv[1]).read().strip()


def part1():
    grid = [line for line in INPUT.strip().split("\n")]

    beam_indexes = [set() for _ in grid]
    splits = 0

    for row_index, row in enumerate(grid):
        for index, char in enumerate(row):
            if char == "S":
                beam_indexes[row_index].add(index)
            elif row_index > 0 and index in beam_indexes[row_index - 1]:
                if char == ".":
                    beam_indexes[row_index].add(index)
                elif char == "^":
                    beam_indexes[row_index].add(index - 1)
                    beam_indexes[row_index].add(index + 1)
                    splits += 1

    return splits


def part2():
    grid = [line for line in INPUT.strip().split("\n")]

    graph = {}  # (row, col) -> set((row, col))
    start = None
    for row_index, row in enumerate(grid):
        for index, char in enumerate(row):
            if char == "S":
                graph[(row_index, index)] = set()
                start = (row_index, index)
            elif row_index > 0 and (row_index - 1, index) in graph:
                if char == ".":
                    graph[(row_index, index)] = set()
                    graph[(row_index - 1, index)].add((row_index, index))
                elif char == "^":
                    graph[(row_index, index - 1)] = set()
                    graph[(row_index - 1, index)].add((row_index, index - 1))
                    graph[(row_index, index + 1)] = set()
                    graph[(row_index - 1, index)].add((row_index, index + 1))

    ends = [k for k in graph.keys() if not graph[k]]

    def count_paths(graph, start, end):
        in_degree = defaultdict(int)
        for node in graph:
            for neighbor in graph[node]:
                in_degree[neighbor] += 1
        # output:
        # {(1, 7): 1, (2, 6): 1, (2, 8): 1, (3, 6): 1, ...}

        # just the start node really
        queue = deque([node for node in graph if in_degree[node] == 0])

        # traverse the tree to build an order
        topo_order = []
        # [(0, 7), (1, 7), (2, 6), (2, 8), (3, 6), (3, 8), (4, 5), ...]

        while queue:
            node = queue.popleft()
            topo_order.append(node)
            for neighbor in graph[node]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        paths = defaultdict(int)
        paths[end] = 1

        for node in reversed(topo_order):
            if node != end:
                for neighbor in graph[node]:
                    paths[node] += paths[neighbor]

        return paths[start]

    total_paths = 0
    for end in ends:
        paths_to_end = count_paths(graph, start, end)
        total_paths += paths_to_end

    return total_paths


print(f"part1: {part1()}")
print(f"part2: {part2()}")
