from utils.parsing import parse_input

Point = tuple[int, int]
Coordinate = tuple[int, int, int, int]
Grid = list[list[str]]


def parse_grid() -> tuple[Grid, Coordinate]:
    grid = []
    guard_position = (-1, -1, 0, 0)
    for line in parse_input():
        if "^" in line:
            guard_position = (line.index("^"), len(grid), 0, -1)
            line = line.replace("^", ".")
        grid.append(list(line))
    return grid, guard_position


def get_guard_path(grid: Grid, start: Coordinate) -> list[Coordinate]:
    path = []
    visited = set()
    x, y, dx, dy = start
    while True:
        path.append((x, y, dx, dy))
        visited.add((x, y, dx, dy))

        x2, y2 = x + dx, y + dy
        if (x2, y2, dx, dy) in visited or x2 < 0 or y2 < 0:
            break

        try:
            value = grid[y2][x2]
        except IndexError:
            break

        if value == ".":
            x, y = x2, y2
            continue

        dx, dy = -dy, dx
    return path


def is_infinite_loop(grid: Grid, start: Coordinate, visited: set[Coordinate]) -> bool:
    """Same logic as above, but without keeping track of the path for performance reasons"""
    x, y, dx, dy = start
    while True:
        visited.add((x, y, dx, dy))

        x2, y2 = x + dx, y + dy
        if (x2, y2, dx, dy) in visited:
            return True

        if x2 < 0 or y2 < 0:
            break

        try:
            value = grid[y2][x2]
        except IndexError:
            break

        if value == ".":
            x, y = x2, y2
            continue

        dx, dy = -dy, dx

    return False


def main1() -> int:
    grid, guard = parse_grid()
    path = get_guard_path(grid, guard)
    return len({(x, y) for x, y, _, _ in path})


def build_visited_cache(
    path: list[Coordinate],
) -> dict[Point, tuple[Coordinate, set[Coordinate]]]:
    res = {}
    visited = {path[0]}
    for i in range(1, len(path)):
        x, y, _, _ = path[i]
        if (x, y) in res:
            continue

        res[(x, y)] = (path[i - 1], visited.copy())
        visited.add(path[i])
    return res


def main2() -> int:
    count = 0
    grid, start = parse_grid()

    path = get_guard_path(grid, start)
    visited_cache = build_visited_cache(path)

    possible_obstacles = visited_cache.keys()
    for x, y in possible_obstacles:
        grid[y][x] = "#"
        start, visited = visited_cache[(x, y)]
        if is_infinite_loop(grid, start, visited=visited):
            count += 1
        grid[y][x] = "."
    return count
