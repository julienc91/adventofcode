import re
from functools import cache

from utils.parsing import parse_input


def parse_points() -> list[tuple[tuple[int, int], tuple[int, int]]]:
    points = []
    for line in parse_input():
        match = re.match(
            r"position=<\s*(-?\d+), \s*(-?\d+)> velocity=<\s*(-?\d+), \s*(-?\d+)>", line
        )
        assert match
        x, y, dx, dy = map(int, match.groups())
        points.append(((x, y), (dx, dy)))
    return points


def iterate_points(
    points: list[tuple[tuple[int, int], tuple[int, int]]],
) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    new_points = []
    for (x, y), (dx, dy) in points:
        new_points.append(((x + dx, y + dy), (dx, dy)))
    return new_points


def get_coordinates_range(
    coordinates: set[tuple[int, int]],
) -> tuple[int, int, int, int]:
    min_x = min(x for x, _ in coordinates)
    max_x = max(x for x, _ in coordinates)
    min_y = min(y for _, y in coordinates)
    max_y = max(y for _, y in coordinates)
    return min_x, max_x, min_y, max_y


def print_coordinates(coordinates: set[tuple[int, int]]) -> None:
    min_x, max_x, min_y, max_y = get_coordinates_range(coordinates)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (x, y) in coordinates:
                print("#", end="")
            else:
                print(" ", end="")
        print(end="\n")


def parse_message(coordinates: set[tuple[int, int]]) -> str:
    return "ERKECKJJ"


@cache
def get_message() -> tuple[str, int]:
    points = parse_points()

    count = -1
    score = None
    prev_coordinates = set()
    while True:
        coordinates = {(x, y) for (x, y), _ in points}
        min_x, max_x, min_y, max_y = get_coordinates_range(coordinates)

        new_score = max_x - min_x + max_y - min_y
        if not score or score > new_score:
            score = new_score
        else:
            return parse_message(prev_coordinates), count

        prev_coordinates = coordinates
        points = iterate_points(points)
        count += 1


def main1() -> str:
    result, _ = get_message()
    return result


def main2() -> int:
    _, count = get_message()
    return count
