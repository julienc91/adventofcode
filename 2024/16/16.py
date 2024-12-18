import heapq
from collections import defaultdict
from collections.abc import Iterator
from functools import cache

from utils.enums import Direction
from utils.graph import get_shortest_path
from utils.parsing import parse_input

Grid = tuple[str, ...]
Point = tuple[int, int]
Position = tuple[int, int, Direction]


def parse_grid() -> Grid:
    return tuple(parse_input())


@cache
def get_min_weight(grid: Grid) -> int:
    start = (1, len(grid) - 2, Direction.RIGHT)
    end = (len(grid[1]) - 2, 1)

    def get_neighbours(
        position: Position, weight: int
    ) -> Iterator[tuple[int, Position]]:
        x, y, direction = position
        x2, y2 = direction.move(x, y)
        next_position = (x2, y2, direction)
        if grid[y2][x2] != "#":
            yield weight + 1, next_position

        for turn in (direction.turn_left(), direction.turn_right()):
            next_position = (x, y, turn)
            yield weight + 1_000, next_position

    def is_over(position: Position) -> bool:
        x, y, _ = position
        return (x, y) == end

    weight, _ = get_shortest_path(start, get_neighbours, is_over)
    return weight


def get_all_shortest_paths(grid: Grid) -> Iterator[tuple[int, tuple[Point, ...]]]:
    start = (1, len(grid) - 2, Direction.RIGHT)
    x, y, _ = start
    queue: list[tuple[int, Position, tuple[Point, ...]]] = [(0, start, ((x, y),))]
    weight_by_position = defaultdict(lambda: float("inf"))
    min_weight = get_min_weight(grid)

    while queue:
        weight, (x, y, direction), path = heapq.heappop(queue)
        if weight > min_weight:
            break

        if grid[y][x] == "E":
            yield weight, path
            continue

        x2, y2 = direction.move(x, y)
        next_position = (x2, y2, direction)
        if grid[y2][x2] != "#" and weight + 1 <= weight_by_position[next_position]:
            weight_by_position[next_position] = weight + 1
            heapq.heappush(queue, (weight + 1, next_position, path + ((x2, y2),)))

        for turn in (direction.turn_left(), direction.turn_right()):
            next_position = (x, y, turn)
            if weight + 1_000 <= weight_by_position[next_position]:
                weight_by_position[next_position] = weight + 1_000
                heapq.heappush(queue, (weight + 1_000, next_position, path))


def main1() -> int:
    grid = parse_grid()
    return get_min_weight(grid)


def main2() -> int:
    grid = parse_grid()
    visited = set()
    for _, path in get_all_shortest_paths(grid):
        visited |= set(path)
    return len(visited)
