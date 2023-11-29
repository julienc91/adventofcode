from collections import defaultdict
from collections.abc import Iterator
from enum import Enum

from utils.parsing import parse_input


class State(Enum):
    AIR = "."
    ROCK = "#"
    SAND = "o"


def parse_grid() -> dict[tuple[int, int], State]:
    grid: dict[tuple[int, int], State] = defaultdict(lambda: State.AIR)
    for line in parse_input():
        coordinates = [tuple(map(int, item.split(","))) for item in line.split(" -> ")]
        x1, y1 = coordinates.pop(0)
        while coordinates:
            x2, y2 = coordinates.pop(0)
            if x1 == x2:
                for y in range(min(y1, y2), max(y1, y2) + 1):
                    grid[(x1, y)] = State.ROCK
            else:
                for x in range(min(x1, x2), max(x1, x2) + 1):
                    grid[(x, y1)] = State.ROCK
            x1, y1 = x2, y2
    return grid


def make_sand(grid: dict[tuple[int, int], State], with_floor: bool) -> Iterator[None]:
    max_y = max(y for x, y in grid if grid[(x, y)] == State.ROCK)
    if with_floor:
        max_y += 2

    while True:
        x, y = 500, 0
        while y <= max_y:
            if with_floor:
                grid[(x, max_y)] = grid[(x + 1, max_y)] = grid[
                    (x - 1, max_y)
                ] = State.ROCK

            if grid[(x, y + 1)] == State.AIR:
                y += 1
            elif grid[(x - 1, y + 1)] == State.AIR:
                y += 1
                x -= 1
            elif grid[(x + 1, y + 1)] == State.AIR:
                y += 1
                x += 1
            else:
                if grid[(x, y)] != State.AIR:
                    return

                grid[(x, y)] = State.SAND
                yield
                break
        else:
            break


def print_grid(grid: dict[tuple[int, int], State]) -> None:
    ymin = 0
    ymax = max(y for x, y in grid if grid[(x, y)] != State.AIR)

    xmin = min(x for x, y in grid if grid[(x, y)] != State.AIR)
    xmax = max(x for x, y in grid if grid[(x, y)] != State.AIR)

    for y in range(ymin, ymax + 2):
        for x in range(xmin - 2, xmax + 2):
            print(grid[(x, y)].value, end="")
        print("", end="\n")
    print()


def main1() -> int:
    grid = parse_grid()

    count_sand = 0
    for _ in make_sand(grid, with_floor=False):
        count_sand += 1
    return count_sand


def main2() -> int:
    grid = parse_grid()

    count_sand = 0
    for _ in make_sand(grid, with_floor=True):
        count_sand += 1
    return count_sand
