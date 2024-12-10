from collections.abc import Callable

from utils.parsing import parse_input

HikingTrail = tuple[tuple[int, int], ...]


def parse_map() -> list[list[int]]:
    return list(list(map(int, line)) for line in parse_input())


def get_hiking_trails(grid: list[list[int]], x: int, y: int) -> set[HikingTrail]:
    visited_paths = set()
    queue: list[tuple[int, int, HikingTrail]] = [(x, y, ())]
    while queue:
        x, y, path = queue.pop(0)
        value = grid[y][x]
        path = path + ((x, y),)

        if value == 9:
            visited_paths.add(path)
            continue

        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            x2, y2 = x + dx, y + dy
            if x2 < 0 or y2 < 0 or y2 >= len(grid) or x2 >= len(grid[y2]):
                continue

            if grid[y2][x2] != value + 1:
                continue

            queue.append((x2, y2, path))

    return visited_paths


def _main(get_score: Callable[[set[HikingTrail]], int]) -> int:
    score = 0
    grid = parse_map()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                hiking_trails = get_hiking_trails(grid, x, y)
                score += get_score(hiking_trails)
    return score


def main1() -> int:
    return _main(lambda hiking_trails: len({trail[-1] for trail in hiking_trails}))


def main2() -> int:
    return _main(lambda hiking_trails: len(hiking_trails))
