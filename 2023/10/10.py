from utils.enums import Direction
from utils.parsing import parse_input


def _solve_for_start_type(
    grid: list[str], start: tuple[int, int], start_type: str
) -> list[tuple[int, int]] | None:
    x, y = start
    directions_by_pipe_type = {
        "|": (Direction.TOP, Direction.BOTTOM),
        "-": (Direction.LEFT, Direction.RIGHT),
        "L": (Direction.TOP, Direction.RIGHT),
        "J": (Direction.TOP, Direction.LEFT),
        "7": (Direction.BOTTOM, Direction.LEFT),
        "F": (Direction.BOTTOM, Direction.RIGHT),
    }
    direction = directions_by_pipe_type[start_type][0]
    expected_final_direction = directions_by_pipe_type[start_type][1].opposite
    path = [start]
    while True:
        x, y = {
            Direction.TOP: (x, y - 1),
            Direction.BOTTOM: (x, y + 1),
            Direction.LEFT: (x - 1, y),
            Direction.RIGHT: (x + 1, y),
        }[direction]

        if not (0 <= y < len(grid) and 0 <= x < len(grid[y])):
            return None

        new_pipe = grid[y][x]
        if new_pipe == "S":
            return path if direction == expected_final_direction else None
        if new_pipe == ".":
            return None
        if direction.opposite not in directions_by_pipe_type[new_pipe]:
            return None

        direction = next(
            dir_
            for dir_ in directions_by_pipe_type[new_pipe]
            if dir_ != direction.opposite
        )
        path.append((x, y))


def find_path(grid: list[str]) -> list[tuple[int, int]]:
    start = next((grid[y].index("S"), y) for y in range(len(grid)) if "S" in grid[y])
    for start_type in "|-LJ7F":
        path = _solve_for_start_type(grid, start, start_type)
        if path is not None:
            return path
    raise RuntimeError("Path not found")


def simplify_grid(grid: list[str], path: list[tuple[int, int]]) -> list[str]:
    path_items = set(path)
    simplified_grid = []
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[y])):
            line += grid[y][x] if (x, y) in path_items else "."
        simplified_grid.append(line)
    return simplified_grid


def compute_area(grid: list[str], path: list[tuple[int, int]]) -> int:
    grid = simplify_grid(grid, path)
    path_items = set(path)
    count = 0
    in_area = False
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if (x, y) in path_items:
                if grid[y][x] in "|LJ":
                    in_area = not in_area
            else:
                count += 1 if in_area else 0
    return count


def print_grid(grid: list[str]) -> None:
    chars = {"7": "┐", "L": "└", "J": "┘", "F": "┌", "-": "─", "|": "|", "S": "S"}
    for y in range(len(grid)):
        line = ""
        for x in range(len(grid[y])):
            line += chars.get(grid[y][x], " ")
        print(line)


def main1() -> int:
    grid = list(parse_input())
    path = find_path(grid)
    return len(path) // 2


def main2() -> int:
    grid = list(parse_input())
    path = find_path(grid)
    return compute_area(grid, path)
