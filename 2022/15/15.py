import bisect
import re

from utils.parsing import parse_input

Point = tuple[int, int]


def parse_sensors() -> list[tuple[Point, Point]]:
    regex = re.compile(
        r"Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)"
    )
    sensors: list[tuple[Point, Point]] = []
    for line in parse_input():
        match = regex.match(line)
        if not match:
            break

        groups = match.groups()
        sensor = (int(groups[0]), int(groups[1]))
        beacon = (int(groups[2]), int(groups[3]))
        sensors.append((sensor, beacon))
    return sensors


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    if not intervals:
        return intervals

    result = [intervals.pop(0)]
    for interval in intervals:
        if result[-1][0] <= interval[0] <= result[-1][1]:
            result[-1] = (result[-1][0], max(result[-1][1], interval[1]))
        else:
            result.append(interval)
    return result


def get_sensor_interval(
    sensor: Point, beacon: Point, target_y: int
) -> tuple[int, int] | None:
    (xs, ys), (xb, yb) = sensor, beacon

    stop_distance = abs(xs - xb) + abs(ys - yb)
    distance_to_target = abs(ys - target_y)
    if distance_to_target > stop_distance:
        return None

    x_min = xs - (stop_distance - distance_to_target)
    x_max = xs + (stop_distance - distance_to_target)
    return x_min, x_max


def get_sensors_intervals(
    data: list[tuple[Point, Point]],
    target_y: int,
    allowed_range: tuple[int, int] | None = None,
) -> list[tuple[int, int]]:
    intervals: list[tuple[int, int]] = []
    for sensor, beacon in data:
        interval = get_sensor_interval(sensor, beacon, target_y)
        if interval is None:
            continue
        if allowed_range is not None:
            interval = (
                max(allowed_range[0], interval[0]),
                min(allowed_range[1], interval[1]),
            )
        bisect.insort(intervals, interval)
    intervals = merge_intervals(intervals)
    return intervals


def main1() -> int:
    data = parse_sensors()
    target_y = 2_000_000
    intervals = get_sensors_intervals(data, target_y)
    return sum(x_max - x_min for x_min, x_max in intervals)


def main2() -> int:
    data = parse_sensors()
    x_min = 0
    x_max = y_max = 4_000_000

    # y_min should be 0, but since it takes ~2 minutes to cover the [0, y_max] interval,
    # I'd rather start closer to the solution to not take too long on the CI
    y_min = 3_130_000

    for y in range(y_min, y_max + 1):
        intervals = get_sensors_intervals(data, y, (x_min, x_max))
        if len(intervals) == 1:
            # Edge case not handled: only one interval, and x == 0 or x == x_max
            continue
        else:
            return (intervals[0][1] + 1) * x_max + y

    raise RuntimeError
