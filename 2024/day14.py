import re
import sys
from typing import NamedTuple

INPUT = open(sys.argv[1]).read().strip()


Point = NamedTuple("Point", [("x", int), ("y", int)])


class Robot:
    def __init__(self, position: Point, velocity: Point, bounds: Point):
        self.position = position
        self.velocity = velocity
        self.bounds = bounds

    def move(self):
        new_x = self.position.x + self.velocity.x
        if new_x < 0:
            new_x = self.bounds.x + new_x
        elif new_x >= self.bounds.x:
            new_x = new_x - self.bounds.x

        new_y = self.position.y + self.velocity.y
        if new_y < 0:
            new_y = self.bounds.y + new_y
        elif new_y >= self.bounds.y:
            new_y = new_y - self.bounds.y

        self.position = Point(new_x, new_y)


def part1():
    bounds = Point(101, 103)
    robots = []
    for line in INPUT.split("\n"):
        px, py, vx, vy = re.match(
            r"p=([\d-]+),([\d-]+) v=([\d-]+),([\d-]+)", line
        ).groups()
        position = Point(int(px), int(py))
        velocity = Point(int(vx), int(vy))

        robot = Robot(position, velocity, bounds)
        robots.append(robot)

    for _ in range(100):
        for robot in robots:
            robot.move()

    robot_positions = {}
    for robot in robots:
        robot_positions.setdefault(robot.position, 0)
        robot_positions[robot.position] += 1

    quad1 = (Point(0, 0), Point(bounds.x // 2, (bounds.y // 2)))
    quad2 = (Point((bounds.x // 2) + 1, 0), Point(bounds.x, (bounds.y // 2)))
    quad3 = (Point(0, (bounds.y // 2) + 1), Point((bounds.x // 2), bounds.y))
    quad4 = (Point((bounds.x // 2) + 1, (bounds.y // 2) + 1), Point(bounds.x, bounds.y))
    quad_counts = []

    for quad_start, quad_end in [quad1, quad2, quad3, quad4]:
        quad_count = 0
        for y_point in range(quad_start.y, quad_end.y):
            for x_point in range(quad_start.x, quad_end.x):
                point = Point(x_point, y_point)
                quad_count += robot_positions.get(point, 0)

        quad_counts.append(quad_count)

    # lines = []
    # for y_point in range(bounds.y):
    #     line = ""
    #     for x_point in range(bounds.x):
    #         count = robot_positions.get(Point(x_point, y_point), 0)

    #         line += str(count) if count else "."
    #     lines.append(line)
    # print("\n".join(lines))

    total_count = 1
    for quad_count in quad_counts:
        total_count = total_count * quad_count
    return total_count


def part2():
    pass


print(part1())
print(part2())
