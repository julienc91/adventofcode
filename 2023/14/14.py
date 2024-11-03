from collections.abc import Iterator

from utils.parsing import parse_input


def tilt(
    round_rocks: set[tuple[int, int]],
    cube_rocks: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    stuck_rocks = set()
    sorted_round_rocks = sorted(round_rocks)
    while sorted_round_rocks:
        x, y = sorted_round_rocks.pop(0)
        while y > 0:
            if (x, y - 1) in stuck_rocks or (x, y - 1) in cube_rocks:
                break
            y -= 1
        stuck_rocks.add((x, y))
    return stuck_rocks


def get_rocks_positions(
    grid: list[str],
) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    round_rocks = set()
    cube_rocks = set()
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "O":
                round_rocks.add((x, y))
            elif grid[y][x] == "#":
                cube_rocks.add((x, y))
    return round_rocks, cube_rocks


def get_load_score(round_rocks: set[tuple[int, int]], max_y: int) -> int:
    return sum(max_y - y for _, y in round_rocks)


def rotate_coordinates(x: int, y: int, max_x: int) -> tuple[int, int]:
    return max_x - y, x


def iterate_load_score(grid: list[str]) -> Iterator[set[tuple[int, int]]]:
    round_rocks, cube_rocks = get_rocks_positions(grid)
    max_x = len(grid) - 1
    assert max_x == len(grid[0]) - 1

    # Pre-compute rotations of cube rocks
    rotated_cube_rocks = [cube_rocks]
    for _ in range(3):
        rotated_cube_rocks.append({(max_x - y, x) for x, y in rotated_cube_rocks[-1]})

    while True:
        for i in range(4):
            cube_rocks = rotated_cube_rocks[i]
            round_rocks = tilt(round_rocks, cube_rocks)
            # Rotate coordinates of round rocks
            round_rocks = {(max_x - y, x) for x, y in round_rocks}
        yield round_rocks


def main1() -> int:
    grid = list(parse_input())
    round_rocks, cube_rocks = get_rocks_positions(grid)
    round_rocks = tilt(round_rocks, cube_rocks)
    return get_load_score(round_rocks, len(grid))


def main2() -> int:
    grid = list(parse_input())
    iterator = iterate_load_score(grid)
    history = {}
    rounds_wanted = 1_000_000_000

    for i in range(rounds_wanted):
        round_rocks = frozenset(next(iterator))
        if round_rocks not in history:
            history[round_rocks] = i + 1
            continue

        cycle_length = i + 1 - history[round_rocks]
        rounds_left_needed = (rounds_wanted - i - 2) % cycle_length
        for _ in range(rounds_left_needed):
            next(iterator)
        break

    return get_load_score(next(iterator), len(grid))
