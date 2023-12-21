import itertools

from utils.enums import Direction
from utils.parsing import parse_input


def parse_grid() -> tuple[list[str], tuple[int, int]]:
    grid: list[str] = list(parse_input())
    start = None
    for x, y in itertools.product(range(len(grid[0])), range(len(grid))):
        c = grid[y][x]
        if c == "S":
            start = (x, y)
            break
    assert start is not None
    return grid, start


def main1() -> int:
    grid, start = parse_grid()
    positions = {start}

    max_x, max_y = len(grid[0]), len(grid)
    for step in range(64):
        new_positions = set()
        for x, y in positions:
            for direction in Direction:
                x2, y2 = direction.move(x, y)
                if x2 < 0 or y2 < 0 or x2 >= max_x or y2 >= max_y:
                    continue
                if grid[y2][x2] == "#":
                    continue
                new_positions.add((x2, y2))
        positions = new_positions
    return len(positions)


def main2() -> int:
    # pattern_size: 131, and 26501365 % pattern_size = 65
    # 1. Compute the values for each x where x % pattern_size == 65
    #   (65, 3957), (196, 35223), (327, 97645), (458, 191223)
    # 2. Compute the polynomial interpolation for the resulting coordinates:
    #   https://www.wolframalpha.com/input?i=interpolating+polynomial+calculator&\
    #       assumption=%7B%22F%22%2C+%22InterpolatingPolynomialCalculator%22%2C+\
    #       %22data2%22%7D+-%3E%22%7B%7B65%2C+3957%7D%2C+%7B196%2C+35223%7D%2C+\
    #       %7B327%2C+97645%7D%2C+%7B458%2C+191223%7D%7D%22
    #   f(x) = 139807/17161 + (29988 x)/17161 + (15578 x^2)/17161
    # 3. Compute the result for x = 26501365
    x = 26501365
    return int(139807 / 17161 + (29988 * x) / 17161 + (15578 * (x**2)) / 17161)
