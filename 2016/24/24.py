import itertools
from collections import deque
from functools import cache

from utils.parsing import parse_input

Point = tuple[int, int]


def parse_map() -> tuple[frozenset[Point], list[Point]]:
    res: set[Point] = set()
    targets: dict[int, Point] = {}

    y = 0
    for line in parse_input():
        for x, c in enumerate(line):
            if c != "#":
                res.add((x, y))
            if c.isdigit():
                targets[int(c)] = (x, y)
        y += 1
    return frozenset(res), [targets[i] for i in range(len(targets))]


@cache
def get_shortest_path(grid: frozenset[Point], a: Point, b: Point) -> int:
    queue: deque[tuple[Point, int]] = deque([(a, 0)])
    visited: set[Point] = {a}

    while queue:
        (x, y), steps = queue.popleft()
        if (x, y) == b:
            return steps

        for dx, dy in ((0, -1), (0, 1), (-1, 0), (1, 0)):
            x2, y2 = x + dx, y + dy
            if (x2, y2) in grid and (x2, y2) not in visited:
                visited.add((x2, y2))
                queue.append(((x2, y2), steps + 1))

    raise RuntimeError("No path found")


def build_shortest_paths(
    grid: frozenset[Point], targets: list[Point]
) -> dict[tuple[Point, Point], int]:
    shortest_paths: dict[tuple[Point, Point], int] = {}

    for a, b in itertools.combinations(targets, 2):
        s = get_shortest_path(grid, a, b)
        shortest_paths[(a, b)] = s
        shortest_paths[(b, a)] = s

    return shortest_paths


def _main(with_return: bool) -> int:
    grid, targets = parse_map()
    shortest_paths = build_shortest_paths(grid, targets)

    min_length = 10**6
    init = targets.pop(0)

    for permutation in itertools.permutations(targets, len(targets)):
        count = 0
        start = init
        if with_return:
            permutation += (init,)

        for target in permutation:
            count += shortest_paths[(start, target)]
            start = target
        min_length = min(min_length, count)

    return min_length


def main1() -> int:
    return _main(False)


def main2() -> int:
    return _main(True)
