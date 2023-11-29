from collections import defaultdict
from collections.abc import Iterator

from utils.parsing import parse_input


def parse_coordinates() -> Iterator[tuple[tuple[int, int], tuple[int, int]]]:
    for line in parse_input():
        c1, c2 = line.split(" -> ")
        x1, y1 = [int(n) for n in c1.split(",")]
        x2, y2 = [int(n) for n in c2.split(",")]
        yield (x1, y1), (x2, y2)


def update_grid_with_coordinates(
    grid: dict[tuple[int, int], int],
    coordinates: tuple[tuple[int, int], tuple[int, int]],
    ignore_diagonals: bool,
) -> None:
    (x1, y1), (x2, y2) = coordinates
    if x1 == x2:
        targets = [(x1, y) for y in range(min(y1, y2), max(y1, y2) + 1)]
    elif y1 == y2:
        targets = [(x, y1) for x in range(min(x1, x2), max(x1, x2) + 1)]
    elif ignore_diagonals:
        return
    else:
        xs = [i for i in range(x1, x2, (1 if x1 < x2 else -1))] + [x2]
        ys = [i for i in range(y1, y2, (1 if y1 < y2 else -1))] + [y2]
        targets = [(x, y) for x, y in zip(xs, ys)]

    for target in targets:
        grid[target] += 1


def _main(ignore_diagonals: bool) -> int:
    grid: dict[tuple[int, int], int] = defaultdict(int)
    for coordinates in parse_coordinates():
        update_grid_with_coordinates(
            grid, coordinates, ignore_diagonals=ignore_diagonals
        )
    result = sum(1 for i in grid.values() if i > 1)
    return result


def main1() -> int:
    return _main(ignore_diagonals=True)


def main2() -> int:
    return _main(ignore_diagonals=False)
