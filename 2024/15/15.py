from collections.abc import Iterator

from utils.enums import Direction
from utils.parsing import parse_input

Grid = list[list[str]]
Swap = tuple[tuple[int, int], tuple[int, int]]


class CannotMove(Exception):
    pass


def parse_grid() -> Grid:
    grid = []
    for line in parse_input(str):
        if not line:
            break
        grid.append(list(line))
    return grid


def expand_grid(grid: Grid) -> Grid:
    mapping = {"#": "##", "O": "[]", ".": "..", "@": "@."}
    return [list("".join(mapping[c] for c in line)) for line in grid]


def parse_instructions() -> Iterator[str]:
    for line in parse_input():
        yield from line


def find_robot_position(grid: Grid) -> tuple[int, int]:
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "@":
                return x, y
    raise RuntimeError("Robot not found")


def _get_direction(instruction: str) -> Direction:
    match instruction:
        case "^":
            return Direction.TOP
        case ">":
            return Direction.RIGHT
        case "v":
            return Direction.BOTTOM
        case "<":
            return Direction.LEFT
    raise ValueError(instruction)


def _move_cell(
    grid: Grid, position: tuple[int, int], direction: Direction, /, swaps: list[Swap]
) -> None:
    x, y = position
    x2, y2 = direction.move(x, y)
    value = grid[y][x]

    next_value = grid[y2][x2]
    if next_value == ".":
        pass
    elif next_value == "O":
        _move_cell(grid, (x2, y2), direction, swaps=swaps)
    elif next_value == "[":
        _move_cell(grid, (x2, y2), direction, swaps=swaps)
        if direction in (Direction.TOP, Direction.BOTTOM):
            _move_cell(grid, (x2 + 1, y2), direction, swaps=swaps)
    elif next_value == "]":
        _move_cell(grid, (x2, y2), direction, swaps=swaps)
        if direction in (Direction.TOP, Direction.BOTTOM):
            _move_cell(grid, (x2 - 1, y2), direction, swaps=swaps)
    else:
        raise CannotMove()

    grid[y2][x2] = value
    grid[y][x] = "."
    swaps.insert(0, ((x, y), (x2, y2)))


def move_robot(
    grid: Grid, position: tuple[int, int], instruction: str
) -> tuple[int, int]:
    x, y = position
    direction = _get_direction(instruction)
    x2, y2 = direction.move(x, y)

    swaps: list[Swap] = []
    try:
        _move_cell(grid, position, direction, swaps=swaps)
        return x2, y2
    except CannotMove:
        for (x1, y1), (x2, y2) in swaps:  # Revert changes
            grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]
        return x, y


def get_gps(grid: Grid) -> int:
    score = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] in "O[":
                score += 100 * y + x
    return score


def _main(expand: bool) -> int:
    grid = parse_grid()
    if expand:
        grid = expand_grid(grid)
    position = find_robot_position(grid)
    for instruction in parse_instructions():
        position = move_robot(grid, position, instruction)

    return get_gps(grid)


def main1() -> int:
    return _main(False)


def main2() -> int:
    return _main(True)
