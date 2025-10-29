from collections import defaultdict

from utils.parsing import parse_input

Point = tuple[int, int]


def parse_points() -> list[Point]:
    points = []
    for line in parse_input():
        x, y = map(int, line.split(", "))
        points.append((x, y))
    return points


def get_grid_size(points: list[Point]) -> tuple[int, int]:
    max_x, max_y = 0, 0
    for x, y in points:
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return max_x + 1, max_y + 1


def main1() -> int:
    points = parse_points()
    max_x, max_y = get_grid_size(points)

    area_sizes: dict[tuple[int, int], int] = defaultdict(int)
    points_with_infinite_areas: set[tuple[int, int]] = set()

    for x in range(max_x):
        for y in range(max_y):
            closest_distance = None
            closest_point = None
            for a, b in points:
                distance = abs(a - x) + abs(b - y)
                if closest_distance is None or distance < closest_distance:
                    closest_distance = distance
                    closest_point = (a, b)
                elif distance == closest_distance:
                    closest_point = None

            if closest_point:
                if x == 0 or y == 0 or x == max_x or y == max_y:
                    points_with_infinite_areas.add(closest_point)
                    area_sizes.pop(closest_point, None)
                elif closest_point not in points_with_infinite_areas:
                    area_sizes[closest_point] += 1

    return max(area_sizes.values())


def main2() -> int:
    points = parse_points()
    max_x, max_y = get_grid_size(points)
    max_distance = 10_000

    count = 0
    for x in range(max_x):
        for y in range(max_y):
            total_distances = 0
            for a, b in points:
                total_distances += abs(a - x) + abs(b - y)
                if total_distances >= max_distance:
                    break
            else:
                count += 1
    return count
