import itertools

from utils.parsing import parse_input


def get_galaxies_positions(
    grid: list[str], expansion_factor: int
) -> list[tuple[int, int]]:
    empty_rows = []
    positions = []
    for i, row in enumerate(grid):
        if "#" not in row:
            empty_rows.append(i)
            continue

        for j, value in enumerate(row):
            if value == "#":
                positions.append((j, i))

    empty_columns = []
    for j in range(len(grid[0])):
        if "#" not in "".join([grid[i][j] for i in range(len(grid))]):
            empty_columns.append(j)

    expanded_positions = []
    for x, y in positions:
        x += sum([expansion_factor - 1 for i in empty_columns if i < x])
        y += sum([expansion_factor - 1 for i in empty_rows if i < y])
        expanded_positions.append((x, y))

    return expanded_positions


def _main(expansion_factor: int) -> int:
    grid = list(parse_input())
    positions = get_galaxies_positions(grid, expansion_factor)
    res = 0
    for a, b in itertools.combinations(positions, 2):
        res += abs(a[0] - b[0]) + abs(a[1] - b[1])
    return res


def main1() -> int:
    return _main(2)


def main2() -> int:
    return _main(1000000)
