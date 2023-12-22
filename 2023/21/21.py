import itertools
from collections.abc import Iterator
from functools import cached_property

from utils.cache import pre_compute
from utils.enums import Direction
from utils.maths import polynomial_interpolation
from utils.parsing import parse_input


class InfiniteGrid:
    def __init__(self, pattern: list[list[str]]) -> None:
        self.pattern = pattern

    @cached_property
    def pattern_size(self) -> tuple[int, int]:
        return len(self.pattern[0]), len(self.pattern)

    def __getitem__(self, item: tuple[int, int]) -> str:
        x, y = item
        max_x, max_y = self.pattern_size
        x %= max_x
        y %= max_y
        return self.pattern[y][x]


def parse_grid() -> tuple[InfiniteGrid, tuple[int, int]]:
    pattern: list[list[str]] = [list(line) for line in parse_input()]
    start = None
    max_x, max_y = len(pattern[0]), len(pattern)
    for x, y in itertools.product(range(max_x), range(max_y)):
        c = pattern[y][x]
        if c == "S":
            start = (x, y)
            pattern[y][x] = "."
            break

    assert start is not None
    return InfiniteGrid(pattern), start


def iterate_steps(grid: InfiniteGrid, start: tuple[int, int]) -> Iterator[int]:
    positions = {start}
    while True:
        new_positions = set()
        for x, y in positions:
            for direction in Direction:
                x2, y2 = direction.move(x, y)
                if grid[(x2, y2)] == "#":
                    continue
                new_positions.add((x2, y2))
        positions = new_positions
        yield len(positions)


def main1() -> int:
    grid, start = parse_grid()
    iterator = iterate_steps(grid, start)
    value = 0
    for step in range(64):
        value = next(iterator)
    return value


def compute_interpolation_coordinates(
    grid: InfiniteGrid, start: tuple[int, int], x: int
) -> list[tuple[int, int]]:
    max_x, max_y = grid.pattern_size
    assert max_x == max_y

    modulo = x % max_x
    coordinates = []
    for i, value in enumerate(iterate_steps(grid, start), start=1):
        if i % max_x == modulo:
            coordinates.append((i, value))
            if len(coordinates) == 3:
                break
    return coordinates


def main2() -> int:
    grid, start = parse_grid()
    x = 26501365
    with pre_compute(
        lambda: compute_interpolation_coordinates(grid, start, x), 2023, 21
    ) as cache:
        coordinates = cache

    res = 0
    for i, coeff in enumerate(polynomial_interpolation(coordinates)):
        res += coeff * (x**i)
    return res
