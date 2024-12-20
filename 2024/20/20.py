from collections.abc import Iterator, Sequence

from utils.enums import Direction
from utils.parsing import parse_input

Grid = list[str]
Point = tuple[int, int]


def parse_grid() -> Grid:
    return list(parse_input())


def find_positions(grid: Grid) -> tuple[Point, Point]:
    start = finish = (-1, -1)
    for y in range(len(grid)):
        if (x := grid[y].find("S")) != -1:
            start = (x, y)
        if (x := grid[y].find("E")) != -1:
            finish = (x, y)
    return start, finish


def get_path_without_cheats(grid: Grid, start: Point, finish: Point) -> list[Point]:
    path = [start, start]
    point = start
    while point != finish:
        x, y = point
        for direction in Direction:
            x2, y2 = direction.move(x, y)
            if (x2, y2) != path[-2] and grid[y2][x2] != "#":
                point = x2, y2
                path.append((x2, y2))
                break
        else:
            raise ValueError()
    return path[1:]


def find_cheats(
    grid: Grid, path: Sequence[Point], depth: int
) -> Iterator[tuple[tuple[Point, Point], int]]:
    index_path = {point: i for i, point in enumerate(path)}
    for x1, y1 in path:
        idx1 = index_path[(x1, y1)]

        min_y2 = max(0, y1 - depth)
        max_y2 = min(len(grid) - 1, y1 + depth)

        for y2 in range(min_y2, max_y2 + 1):
            min_x2 = max(0, x1 - (depth - abs(y2 - y1)))
            max_x2 = min(len(grid[y2]), x1 + (depth - abs(y2 - y1)))

            for x2 in range(min_x2, max_x2 + 1):
                if (x2, y2) not in index_path:
                    continue

                distance = abs(x2 - x1) + abs(y2 - y1)
                idx2 = index_path[(x2, y2)]
                if distance >= (idx2 - idx1):
                    continue
                yield ((x1, y1), (x2, y2)), (idx2 - idx1) - distance


def _main(min_gain: int, depth: int) -> int:
    grid = parse_grid()
    start, finish = find_positions(grid)
    path = get_path_without_cheats(grid, start, finish)
    count = 0
    for _, gain in find_cheats(grid, path, depth):
        if gain >= min_gain:
            count += 1
    return count


def main1() -> int:
    return _main(100, 2)


def main2() -> int:
    return _main(100, 20)
