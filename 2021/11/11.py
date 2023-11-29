from utils.parsing import parse_input


def parse_grid() -> list[list[int]]:
    grid = []
    for data in parse_input():
        grid.append([int(i) for i in data])
    return grid


def do_step(grid: list[list[int]]) -> int:
    h, w = len(grid), len(grid[0])
    cells_to_flash = set()
    cells_flashed = set()

    for y in range(h):
        for x in range(w):
            grid[y][x] += 1
            if grid[y][x] > 9:
                cells_to_flash.add((x, y))

    while cells_to_flash:
        x, y = cells_to_flash.pop()
        adjacent_cells = [
            (x - 1, y - 1),
            (x - 1, y),
            (x - 1, y + 1),
            (x, y - 1),
            (x, y + 1),
            (x + 1, y - 1),
            (x + 1, y),
            (x + 1, y + 1),
        ]
        cells_flashed.add((x, y))
        for x2, y2 in adjacent_cells:
            if x2 < 0 or y2 < 0 or x2 >= w or y2 >= h:
                continue
            grid[y2][x2] += 1
            if grid[y2][x2] > 9 and (x2, y2) not in cells_flashed:
                cells_to_flash.add((x2, y2))

    for x, y in cells_flashed:
        grid[y][x] = 0

    return len(cells_flashed)


def main1() -> int:
    nb_steps = 100
    result = 0
    grid = parse_grid()
    for step in range(nb_steps):
        result += do_step(grid)
    return result


def main2() -> int:
    grid = parse_grid()
    h, w = len(grid), len(grid[0])
    step = 1
    while do_step(grid) < h * w:
        step += 1
    return step
