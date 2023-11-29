from enum import Enum
from functools import cache

from utils.parsing import parse_input


class Direction(Enum):
    TOP = "^"
    RIGHT = ">"
    BOTTOM = "v"
    LEFT = "<"


Point = tuple[int, int]


class Grid:
    def __init__(
        self, width: int, height: int, initial_blizzards: set[tuple[Point, Direction]]
    ) -> None:
        self.width = width
        self.height = height
        self.initial_blizzards = initial_blizzards

    @cache
    def _get_step_n(self, n: int) -> tuple[set[tuple[Point, Direction]], set[Point]]:
        if n == 0:
            return self.initial_blizzards, {
                point for point, _ in self.initial_blizzards
            }

        previous_blizzards, _ = self._get_step_n(n - 1)
        new_blizzards: set[tuple[Point, Direction]] = set()
        for (
            (x, y),
            direction,
        ) in previous_blizzards:
            if direction == Direction.TOP:
                x2, y2 = x, y - 1
                if y2 == 0:
                    y2 = self.height - 2
            elif direction == Direction.RIGHT:
                x2, y2 = x + 1, y
                if x2 == self.width - 1:
                    x2 = 1
            elif direction == Direction.BOTTOM:
                x2, y2 = x, y + 1
                if y2 == self.height - 1:
                    y2 = 1
            elif direction == Direction.LEFT:
                x2, y2 = x - 1, y
                if x2 == 0:
                    x2 = self.width - 2
            else:
                raise ValueError
            new_blizzards.add(((x2, y2), direction))
        return new_blizzards, {point for point, _ in new_blizzards}

    def move(self, start: Point, end: Point) -> int:
        queue: list[tuple[Point, int]] = [(start, 0)]
        visited = set()
        while queue:
            (x, y), count = queue.pop(0)
            if (x, y) == end:
                return count

            count += 1
            blizzards_this_step, denied_positions = self._get_step_n(count)

            for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x, y)]:
                if (
                    (y2 <= 0 or y2 >= self.height - 1)
                    or (x2 <= 0 or x2 >= self.width - 1)
                ) and (x2, y2) not in {start, end}:
                    continue
                if (x2, y2) in denied_positions:
                    continue
                if ((x2, y2), count) in visited:
                    continue
                visited.add(((x2, y2), count))
                queue.append(((x2, y2), count))

        raise RuntimeError


def parse_data() -> tuple[Point, Point, Grid]:
    width, height = 0, 0
    start, end = (0, 0), (0, 0)
    blizzards: set[tuple[Point, Direction]] = set()
    for line in parse_input():
        if line[-3] == "#":
            if start == (0, 0):
                width = len(line)
                start = (line.index("."), height)
            else:
                end = (line.index("."), height)
        else:
            for x, c in enumerate(line):
                if c == "." or c == "#":
                    continue
                else:
                    blizzards.add(((x, height), Direction(c)))
        height += 1
    return start, end, Grid(width, height, blizzards)


def main1() -> int:
    start, end, grid = parse_data()
    return grid.move(start, end)


def main2() -> int:
    start, end, grid = parse_data()
    return grid.move(start, end) + grid.move(end, start) + grid.move(start, end)
