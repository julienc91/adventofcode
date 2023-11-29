from utils.parsing import parse_input


def parse_grid() -> list[list[bool]]:
    grid: list[list[bool]] = []
    for line in parse_input():
        grid.append([c == "#" for c in line])
    return grid


def get_new_state(x: int, y: int, grid: list[list[bool]]) -> bool:
    neighbours = (
        (x - 1, y - 1),
        (x, y - 1),
        (x + 1, y - 1),
        (x - 1, y),
        (x + 1, y),
        (x - 1, y + 1),
        (x, y + 1),
        (x + 1, y + 1),
    )
    current_state = grid[y][x]
    nb_neighbours_on = 0
    for a, b in neighbours:
        if a < 0 or b < 0:
            continue
        try:
            nb_neighbours_on += 1 if grid[b][a] else 0
        except IndexError:
            continue
    if current_state is False:
        return nb_neighbours_on == 3
    return nb_neighbours_on in (2, 3)


def do_step(grid: list[list[bool]]) -> list[list[bool]]:
    new_grid: list[list[bool]] = []
    for y in range(len(grid)):
        new_grid.append([])
        row = grid[y]
        for x in range(len(row)):
            new_grid[-1].append(get_new_state(x, y, grid))
    return new_grid


def main1() -> int:
    grid = parse_grid()
    for _ in range(100):
        grid = do_step(grid)
    return sum(1 for row in grid for cell in row if cell)


def main2() -> int:
    grid = parse_grid()
    corners = ((0, 0), (0, -1), (-1, 0), (-1, -1))

    for _ in range(100):
        grid = do_step(grid)
        for x, y in corners:
            grid[y][x] = True
    return sum(1 for row in grid for cell in row if cell)
