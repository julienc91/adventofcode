from collections.abc import Iterator

from utils.enums import Direction
from utils.parsing import parse_input


def find_next_step(
    grid: list[str], position: tuple[int, int], current_direction: Direction
) -> tuple[tuple[int, int], Direction] | None:
    x, y = position

    def inner(direction: Direction) -> tuple[int, int] | None:
        next_cell = (x2, y2) = direction.move(x, y)
        if x2 < 0 or y2 < 0 or y2 >= len(grid) or x2 >= len(grid[y2]):
            return None

        value = grid[y2][x2]
        if value == " ":
            return None
        return next_cell

    directions_to_try = [current_direction] + [
        direction
        for direction in Direction
        if direction not in (current_direction, current_direction.opposite)
    ]
    for direction_to_try in directions_to_try:
        next_position = inner(direction_to_try)
        if next_position is not None:
            return next_position, direction_to_try
    return None


def find_path(grid: list[str]) -> Iterator[tuple[int, int]]:
    position = (grid[0].index("|"), 0)
    yield position

    direction = Direction.BOTTOM

    while True:
        next_step = find_next_step(grid, position, direction)
        if next_step is None:
            break

        position, direction = next_step
        yield position


def main1() -> str:
    grid = list(parse_input())
    res = ""
    for x, y in find_path(grid):
        value = grid[y][x]
        if value not in "-|+":
            res += value
    return res


def main2() -> int:
    grid = list(parse_input())
    return len(list(find_path(grid)))
