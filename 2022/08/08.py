import math

from utils.parsing import parse_input


def get_grid() -> list[list[int]]:
    grid: list[list[int]] = []
    for line in parse_input():
        row = [int(c) for c in line]
        grid.append(row)
    return grid


def main1() -> int:
    grid = get_grid()
    total_visible = 0
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            value = grid[y][x]
            if (
                all(grid[y][x2] < value for x2 in range(x + 1, len(row)))
                or all(grid[y][x2] < value for x2 in range(x - 1, -1, -1))
                or all(grid[y2][x] < value for y2 in range(y + 1, len(grid)))
                or all(grid[y2][x] < value for y2 in range(y - 1, -1, -1))
            ):
                total_visible += 1
    return total_visible


def main2() -> int:
    grid = get_grid()
    best_score = 0
    for y in range(len(grid)):
        row = grid[y]
        for x in range(len(row)):
            value = grid[y][x]
            counters = [0, 0, 0, 0]

            for x2 in range(x + 1, len(row)):
                counters[0] += 1
                if grid[y][x2] >= value:
                    break

            for x2 in range(x - 1, -1, -1):
                counters[1] += 1
                if grid[y][x2] >= value:
                    break

            for y2 in range(y + 1, len(grid)):
                counters[2] += 1
                if grid[y2][x] >= value:
                    break

            for y2 in range(y - 1, -1, -1):
                counters[3] += 1
                if grid[y2][x] >= value:
                    break

            score = math.prod(counters)
            best_score = max(score, best_score)

    return best_score
