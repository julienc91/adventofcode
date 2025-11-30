import math


def get_power_level(x: int, y: int, serial_number: int) -> int:
    rack_id = x + 1 + 10
    power_level = rack_id * (y + 1)
    power_level += serial_number
    power_level *= rack_id
    power_level = ((power_level % 1000) // 100) - 5
    return power_level


def get_power_levels() -> list[list[int]]:
    serial_number = int(input())
    return [
        [get_power_level(x, y, serial_number) for x in range(300)] for y in range(300)
    ]


def build_summed_area_table(grid, size=300):
    sat = [[0] * size for _ in range(size)]
    for y in range(size):
        row_sum = 0
        for x in range(size):
            row_sum += grid[y][x]
            sat[y][x] = row_sum
            if y > 0:
                sat[y][x] += sat[y - 1][x]
    return sat


def rect_sum(sat, x1, y1, x2, y2):
    total = sat[y2][x2]
    if x1 > 0:
        total -= sat[y2][x1 - 1]
    if y1 > 0:
        total -= sat[y1 - 1][x2]
    if x1 > 0 and y1 > 0:
        total += sat[y1 - 1][x1 - 1]
    return total


def main1() -> str:
    power_levels = get_power_levels()

    res = ""
    max_square_score = 0
    square_size = 3
    for x in range(300 - square_size + 1):
        for y in range(300 - square_size + 1):
            square_score = 0
            for dx in range(3):
                for dy in range(3):
                    square_score += power_levels[y + dy][x + dx]
            if square_score > max_square_score:
                max_square_score = square_score
                res = f"{x + 1},{y + 1}"
    return res


def main2() -> str:
    power_levels = get_power_levels()
    size = 300
    sat = build_summed_area_table(power_levels, size)

    best_square_score = -math.inf
    res = ""

    for s in range(1, size + 1):
        limit = size - s + 1
        for y in range(limit):
            for x in range(limit):
                square_score = rect_sum(sat, x, y, x + s - 1, y + s - 1)
                if square_score > best_square_score:
                    best_square_score = square_score
                    res = f"{x + 1},{y + 1},{s}"
    return res
