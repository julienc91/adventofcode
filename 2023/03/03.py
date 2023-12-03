import itertools
import math
import re
from collections import defaultdict
from collections.abc import Iterator
from functools import cache

from utils.parsing import parse_input


@cache
def is_symbol(c: str) -> bool:
    return c not in set("0123456789.")


def find_part_numbers() -> Iterator[tuple[int, set[tuple[int, int]]]]:
    grid = list(parse_input())

    for y in range(len(grid)):
        line = grid[y]

        for match in re.finditer(r"\d+", line):
            number = int(match.group())
            gears = set()

            y_range = list(range(y - 1, y + 2))
            x_range = list(range(match.start() - 1, match.end() + 1))
            is_part_number = False

            for x2, y2 in itertools.product(x_range, y_range):
                if x2 < 0 or y2 < 0 or x2 >= len(line) or y2 >= len(grid):
                    continue

                if is_symbol(grid[y2][x2]):
                    is_part_number = True

                if grid[y2][x2] == "*":
                    gears.add((x2, y2))

            if is_part_number:
                yield number, gears


def main1() -> int:
    return sum(number for number, _ in find_part_numbers())


def main2() -> int:
    all_gears = defaultdict(list)
    for number, adjacent_gears in find_part_numbers():
        for gear in adjacent_gears:
            all_gears[gear].append(number)

    return sum(
        math.prod(numbers) for numbers in all_gears.values() if len(numbers) == 2
    )
