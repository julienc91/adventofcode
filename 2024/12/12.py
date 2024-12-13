import itertools

from utils.parsing import parse_input

Point = tuple[int, int]


def parse_grid() -> list[str]:
    return list(parse_input())


def visit_region(
    grid: list[str], x: int, y: int
) -> tuple[set[Point], list[Point], list[Point]]:
    value = grid[y][x]
    queue = {(x, y)}
    region = set()
    x_borders, y_borders = [], []
    while queue:
        x, y = queue.pop()
        if (x, y) in region:
            continue

        region.add((x, y))
        if y + 1 >= len(grid) or grid[y + 1][x] != value:
            x_borders.append((x, y + 1))
        else:
            queue.add((x, y + 1))

        if y - 1 < 0 or grid[y - 1][x] != value:
            x_borders.append((x, y))
        else:
            queue.add((x, y - 1))

        if x + 1 >= len(grid[y]) or grid[y][x + 1] != value:
            y_borders.append((x + 1, y))
        else:
            queue.add((x + 1, y))

        if x - 1 < 0 or grid[y][x - 1] != value:
            y_borders.append((x, y))
        else:
            queue.add((x - 1, y))

    return region, x_borders, y_borders


def main1() -> int:
    visited = set()
    grid = parse_grid()
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) not in visited:
                region, x_borders, y_borders = visit_region(grid, x, y)
                visited |= region
                total += (len(x_borders) + len(y_borders)) * len(region)
    return total


def count_sides(x_borders: list[Point], y_borders: list[Point]) -> int:
    # Count horizontal sides
    x_borders.sort(key=lambda point: (point[1], point[0]))
    nb_sides = 1
    for (x1, y1), (x2, y2) in itertools.pairwise(x_borders):
        if y2 != y1 or x2 != x1 + 1 or (x2, y2) in y_borders:
            nb_sides += 1

    # Count vertical sides
    y_borders.sort(key=lambda point: (point[0], point[1]))
    nb_sides += 1
    for (x1, y1), (x2, y2) in itertools.pairwise(y_borders):
        if x2 != x1 or y2 != y1 + 1 or (x2, y2) in x_borders:
            nb_sides += 1

    return nb_sides


def main2() -> int:
    visited = set()
    grid = parse_grid()
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) not in visited:
                region, x_borders, y_borders = visit_region(grid, x, y)
                visited |= region
                total += count_sides(x_borders, y_borders) * len(region)
    return total
