import itertools

from utils.parsing import parse_input


def parse_grid() -> list[str]:
    return list(parse_input())


def find_word_at_coordinates(
    grid: list[str], x: int, y: int, dx: int, dy: int, word: str
) -> bool:
    for i, c in enumerate(word):
        x2, y2 = x + i * dx, y + i * dy
        if (
            x2 < 0
            or y2 < 0
            or y2 >= len(grid)
            or x2 >= len(grid[y2])
            or grid[y2][x2] != c
        ):
            return False
    return True


def search_xmas_from_coordinates(grid: list[str], x: int, y: int) -> int:
    count = 0
    for dx, dy in itertools.product((-1, 0, 1), repeat=2):
        if find_word_at_coordinates(grid, x, y, dx, dy, "XMAS"):
            count += 1
    return count


def main1() -> int:
    count = 0
    grid = parse_grid()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            count += search_xmas_from_coordinates(grid, x, y)
    return count


def search_x_mas_from_coordinates(grid: list[str], x: int, y: int) -> bool:
    dx, dy = 1, 1
    return (
        find_word_at_coordinates(grid, x, y, dx, dy, "MAS")
        or find_word_at_coordinates(grid, x, y, dx, dy, "SAM")
    ) and (
        find_word_at_coordinates(grid, x + 2, y, -dx, dy, "MAS")
        or find_word_at_coordinates(grid, x + 2, y, -dx, dy, "SAM")
    )


def main2() -> int:
    count = 0
    grid = parse_grid()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            count += search_x_mas_from_coordinates(grid, x, y)
    return count
