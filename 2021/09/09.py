def is_low_point(x: int, y: int, grid: list[list[int]]) -> bool:
    adjacent_cells = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
    for a, b in adjacent_cells:
        if a < 0 or b < 0:
            continue

        try:
            if grid[a][b] <= grid[x][y]:
                return False
        except IndexError:
            continue
    return True


def fill_bassin(
    x: int, y: int, bassin_id: int, grid: list[list[int]], bassins: list[list[int]]
) -> int:
    adjacent_cells = [(x, y + 1), (x, y - 1), (x + 1, y), (x - 1, y)]
    bassins[x][y] = bassin_id
    res = 1
    for a, b in adjacent_cells:
        if a < 0 or b < 0:
            continue

        try:
            if grid[a][b] == 9:
                continue
            elif bassins[a][b] != bassin_id:
                assert bassins[a][b] == -1, bassins[a][b]
                res += fill_bassin(a, b, bassin_id, grid, bassins)
        except IndexError:
            continue
    return res


def parse_grid() -> list[list[int]]:
    grid: list[list[int]] = []
    try:
        while line := input():
            grid.append([int(i) for i in line.strip()])
    except EOFError:
        pass
    return grid


def main1() -> int:
    grid = parse_grid()
    return sum(
        1 + grid[i][j]
        for i in range(len(grid))
        for j in range(len(grid[i]))
        if is_low_point(i, j, grid)
    )


def main2() -> int:
    grid = parse_grid()
    w, h = len(grid), len(grid[0])
    bassin_id = 0

    bassins: list[list[int]] = [[-1 for _ in range(w)] for _ in range(h)]
    bassin_sizes: list[int] = []
    for i in range(w):
        for j in range(h):
            if grid[i][j] == 9 or bassins[i][j] >= 0:
                continue
            bassin_size = fill_bassin(i, j, bassin_id, grid, bassins)
            bassin_id += 1
            bassin_sizes.append(bassin_size)

    bassin_sizes.sort(reverse=True)
    return bassin_sizes[0] * bassin_sizes[1] * bassin_sizes[2]
