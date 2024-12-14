import re
from collections.abc import Iterator
from functools import reduce
from operator import mul

from utils.parsing import parse_input


def parse_robots() -> Iterator[tuple[int, int, int, int]]:
    for line in parse_input():
        x, y, dx, dy = map(int, re.findall(r"(-?\d+)", line))
        yield x, y, dx, dy


def get_quadrant(x: int, y: int, size: tuple[int, int]) -> tuple[int, int] | None:
    w, h = size
    if x == w // 2 or y == h // 2:
        return None
    return int(x > w // 2), int(y > h // 2)


def elapse_time(
    x: int, y: int, dx: int, dy: int, size: tuple[int, int], seconds: int
) -> tuple[int, int]:
    w, h = size
    return (x + dx * seconds) % w, (y + dy * seconds) % h


def main1() -> int:
    w, h = 101, 103
    count_by_quadrant = {(0, 0): 0, (1, 0): 0, (0, 1): 0, (1, 1): 0}
    for x, y, dx, dy in parse_robots():
        x, y = elapse_time(x, y, dx, dy, size=(w, h), seconds=100)
        quadrant = get_quadrant(x, y, size=(w, h))
        if quadrant:
            count_by_quadrant[quadrant] += 1
    return reduce(mul, count_by_quadrant.values())


def print_grid(positions: set[tuple[int, int]], size: tuple[int, int]) -> None:
    w, h = size
    for y in range(h):
        for x in range(w):
            if (x, y) in positions:
                print("X", end="")
            else:
                print(" ", end="")
        print()
    print()


def main2() -> int:
    w, h = 101, 103
    robots = list(parse_robots())
    seconds = 1
    while True:
        positions = set()
        for x, y, dx, dy in robots:
            position = elapse_time(x, y, dx, dy, size=(w, h), seconds=seconds)
            if position in positions:
                break
            positions.add(position)
        else:
            # assumption: this is the one
            return seconds

        seconds += 1
