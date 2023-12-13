from collections.abc import Iterator

from utils.parsing import parse_input


def parse_grids() -> Iterator[list[str]]:
    grid = []
    for line in parse_input():
        if not line:
            yield grid
            grid = []
        else:
            grid.append(line)
    yield grid


def find_mirror_position(grid: list[str], smudge: bool) -> int | None:
    for y in range(1, len(grid)):
        allow_error = smudge
        for i in range(len(grid)):
            if (y - i - 1 < 0) or (y + i > len(grid) - 1):
                continue

            if grid[y - i - 1] != grid[y + i]:
                if not allow_error:
                    break
                elif count_diffs(grid[y - i - 1], grid[y + i]) > 1:
                    break
                allow_error = False
        else:
            if not allow_error:
                return y

    return None


def find_mirror_value(grid: list[str], smudge: bool) -> int:
    y = find_mirror_position(grid, smudge)
    if y is not None:
        return y * 100

    grid = rotate_grid(grid)
    y = find_mirror_position(grid, smudge)
    if y is not None:
        return y

    raise RuntimeError("Could not find mirror")


def count_diffs(s1: str, s2: str) -> int:
    return sum(1 for c1, c2 in zip(s1, s2) if c1 != c2)


def rotate_grid(grid: list[str]) -> list[str]:
    return ["".join(row) for row in zip(*grid[::-1])]


def _main(smudge: bool) -> int:
    return sum(find_mirror_value(grid, smudge) for grid in parse_grids())


def main1() -> int:
    return _main(False)


def main2() -> int:
    return _main(True)
