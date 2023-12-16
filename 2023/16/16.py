import random

from utils.enums import Direction
from utils.parsing import parse_input


def get_next_positions(
    grid: list[str], position: tuple[int, int, Direction]
) -> list[tuple[int, int, Direction]]:
    x, y, direction = position
    x, y = direction.move(x, y)
    if y < 0 or x < 0:
        return []

    try:
        value = grid[y][x]
    except IndexError:
        return []

    match (value, direction):
        case ("|", Direction.LEFT) | ("|", Direction.RIGHT):
            directions = [Direction.TOP, Direction.BOTTOM]
        case ("-", Direction.TOP) | ("-", Direction.BOTTOM):
            directions = [Direction.LEFT, Direction.RIGHT]
        case ("/", Direction.RIGHT) | ("\\", Direction.LEFT):
            directions = [direction.TOP]
        case ("/", Direction.LEFT) | ("\\", Direction.RIGHT):
            directions = [direction.BOTTOM]
        case ("/", Direction.TOP) | ("\\", Direction.BOTTOM):
            directions = [Direction.RIGHT]
        case ("/", Direction.BOTTOM) | ("\\", Direction.TOP):
            directions = [Direction.LEFT]
        case _:
            directions = [direction]

    return [(x, y, direction) for direction in directions]


__cache = {}


def follow_light_beam(
    grid: list[str], initial: tuple[int, int, Direction]
) -> set[tuple[int, int, Direction]]:
    light_beams = [initial]
    visited = set()

    while light_beams:
        position = light_beams.pop()
        if position in __cache:
            visited |= __cache[position]
            continue

        for new_position in get_next_positions(grid, position):
            if new_position not in visited:
                light_beams.append(new_position)
                visited.add(new_position)

    __cache[initial] = visited
    return visited


def count_energized(visited: set[tuple[int, int, Direction]]) -> int:
    return len({(x, y) for x, y, _ in visited})


def main1() -> int:
    grid = list(parse_input())
    visited = follow_light_beam(grid, (-1, 0, Direction.RIGHT))
    return count_energized(visited)


def main2() -> int:
    grid = list(parse_input())

    # Optimisation: pre-cache results from random starting points
    for _ in range(2 * len(grid)):
        y = random.randrange(0, len(grid))
        x = random.randrange(0, len(grid[y]))
        direction = random.choice(list(Direction))
        _ = follow_light_beam(grid, (x, y, direction))

    # Iterate over each border
    res = 0
    for x in range(len(grid[0])):
        visited = follow_light_beam(grid, (x, -1, Direction.BOTTOM))
        res = max(res, count_energized(visited))

    for x in range(len(grid[0])):
        visited = follow_light_beam(grid, (x, len(grid), Direction.TOP))
        res = max(res, count_energized(visited))

    for y in range(len(grid)):
        visited = follow_light_beam(grid, (-1, y, Direction.RIGHT))
        res = max(res, count_energized(visited))

    for y in range(len(grid)):
        visited = follow_light_beam(grid, (len(grid[y]), y, Direction.LEFT))
        res = max(res, count_energized(visited))
    return res
