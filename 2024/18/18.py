from collections.abc import Iterator

from utils.enums import Direction
from utils.graph import get_shortest_path
from utils.parsing import parse_input


def parse_cells() -> list[tuple[int, int]]:
    res = []
    for line in parse_input():
        a, b = map(int, line.split(","))
        res.append((a, b))
    return res


def get_min_steps_count(corrupted_cells: set[tuple[int, int]]) -> int:
    start = (0, 0)
    finish = (w, h) = (70, 70)

    def get_neighbours(
        cell: tuple[int, int], weight: int
    ) -> Iterator[tuple[int, tuple[int, int]]]:
        x, y = cell
        for direction in [
            Direction.TOP,
            Direction.RIGHT,
            Direction.BOTTOM,
            Direction.LEFT,
        ]:
            x2, y2 = direction.move(x, y)
            if y2 < 0 or y2 > h or x2 < 0 or x2 > w:
                continue

            if (x2, y2) in corrupted_cells:
                continue

            yield weight + 1, (x2, y2)

    weight, _ = get_shortest_path(
        start,
        get_neighbours,
        lambda cell: cell == finish,
    )
    return weight


def main1() -> int:
    corrupted_cells = set(parse_cells()[:1024])
    return get_min_steps_count(corrupted_cells)


def main2() -> str:
    all_cells = parse_cells()
    min_idx, max_idx = 0, len(all_cells) - 1
    n = 0

    while min_idx < max_idx:
        n = (max_idx - min_idx) // 2 + min_idx
        corrupted_cells = set(all_cells[:n])
        try:
            get_min_steps_count(corrupted_cells)
        except RuntimeError:
            max_idx = n
        else:
            min_idx = n + 1

    x, y = all_cells[n - 1]
    return f"{x},{y}"
