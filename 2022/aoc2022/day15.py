import re
from dataclasses import dataclass
from io import StringIO
from timeit import default_timer as timer
from typing import Generator, Iterable, NamedTuple, Tuple

from .inputs import DATA_DIR


INPUT_FILE = DATA_DIR / "input_15.txt"
INPUT_REGEX = re.compile(
    "Sensor at x=(?P<sensorx>-?[0-9]+), y=(?P<sensory>-?[0-9]+): closest beacon is at x=(?P<beaconx>-?[0-9]+), y=(?P<beacony>-?[0-9]+)"
)


class Point(NamedTuple):
    x: int
    y: int


@dataclass
class Sensor:
    location: Point
    beacon: Point

    def coverage_at_row(self, y: int) -> Tuple[int | None, int | None]:
        distance = abs(self.location.x - self.beacon.x) + abs(
            self.location.y - self.beacon.y
        )
        if self.location.y - distance <= y <= self.location.y + distance:
            y_mod = abs(y - self.location.y)
            x_mod = distance - y_mod
            return (self.location.x - x_mod, self.location.x + x_mod + 1)

        return (None, None)


def parse_input(input: StringIO) -> list[Sensor]:
    sensors = []

    for line in input:
        line_values = INPUT_REGEX.match(line).groupdict()
        sensor_location = Point(
            x=int(line_values["sensorx"]), y=int(line_values["sensory"])
        )
        beacon_location = Point(
            x=int(line_values["beaconx"]), y=int(line_values["beacony"])
        )

        sensors.append(Sensor(location=sensor_location, beacon=beacon_location))

    return sensors


def scan_row(sensors: Iterable[Sensor], y: int, min_x: int, max_x: int):
    sensor_ranges = []
    for sensor in sensors:
        sensor_start_x, sensor_end_x = sensor.coverage_at_row(y)
        if sensor_start_x is not None and sensor_end_x is not None:
            sensor_ranges.append((sensor_start_x, sensor_end_x))

    x = min_x
    for sensor_start_x, sensor_end_x in sorted(sensor_ranges, key=lambda r: r[0]):
        if sensor_start_x <= x:
            x = max(x, sensor_end_x)

    if x < max_x:
        for sensor in sensors:
            if (sensor.location.y == y and sensor.location.x == x) or (
                sensor.beacon.y == y and sensor.beacon.x == x
            ):
                return scan_row(sensors, y, x + 1, max_x)

        return Point(x=x, y=y)

    return None


def solve_a(input: StringIO, y: int) -> int:
    sensors = parse_input(input)
    empty_points = set()
    for sensor in sensors:
        sensor_start_x, sensor_end_x = sensor.coverage_at_row(y)
        if sensor_start_x is not None and sensor_end_x is not None:
            empty_points.update(range(sensor_start_x, sensor_end_x))

    sensor_points, beacon_points = set(), set()
    for sensor in sensors:
        if sensor.location.y == y:
            sensor_points.add(sensor.location.x)
        if sensor.beacon.y == y:
            beacon_points.add(sensor.beacon.x)

    return len(empty_points.difference(sensor_points, beacon_points))


def solve_b(input: StringIO, min_x: int, min_y: int, max_x: int, max_y: int) -> int:
    sensors = parse_input(input)

    rows = range(min_y, max_y + 1)
    point = None
    for y in rows:
        point = scan_row(sensors, y, min_x, max_x)
        if point:
            break

    return (point.x * 4000000) + point.y


if __name__ == "__main__":
    start_a = timer()
    input = INPUT_FILE.open("r")
    solution_a = solve_a(input, 2000000)
    end_a = timer()
    print(f"Part 1: {solution_a} (time: {(end_a - start_a) * 1000.0:.6f}ms)")

    input.seek(0)
    start_b = timer()
    solution_b = solve_b(input, 0, 0, 4000000, 4000000)
    end_b = timer()
    print(f"Part 2: {solution_b} (time: {(end_b - start_b) * 1000.0:.6f}ms)")
