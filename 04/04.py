GRID_SIZE = 5


def parse_grids() -> list[list[tuple[int, bool]]]:
    grids = []
    try:
        while True:
            _ = input()
            grid = [(int(i), False) for _ in range(GRID_SIZE) for i in input().split()]
            grids.append(grid)
    except EOFError:
        return grids


def update_grid_with_picked_number(
    grid: list[tuple[int, bool]], picked_number: int
) -> bool:
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            index = y * GRID_SIZE + x
            if grid[index][0] == picked_number:
                grid[index] = (picked_number, True)
                return is_column_completed(grid, x) or is_row_completed(grid, y)
    return False


def is_column_completed(grid: list[tuple[int, bool]], column: int) -> bool:
    for y in range(GRID_SIZE):
        if not grid[y * GRID_SIZE + column][1]:
            return False
    return True


def is_row_completed(grid: list[tuple[int, bool]], row: int) -> bool:
    for x in range(GRID_SIZE):
        if not grid[row * GRID_SIZE + x][1]:
            return False
    return True


def get_grid_score(grid: list[tuple[int, bool]], last_picked_number: int) -> int:
    return sum(value for value, is_marked in grid if not is_marked) * last_picked_number


def main1() -> int:
    picked_numbers = [int(value) for value in input().split(",")]
    grids = parse_grids()
    for number in picked_numbers:
        for grid in grids:
            is_winner = update_grid_with_picked_number(grid, number)
            if is_winner:
                return get_grid_score(grid, number)
    raise RuntimeError


def main2() -> int:
    picked_numbers = [int(value) for value in input().split(",")]
    grids = parse_grids()
    last_won_grid = None
    for number in picked_numbers:
        remaining_grids = []
        for grid in grids:
            is_winner = update_grid_with_picked_number(grid, number)
            if is_winner:
                last_won_grid = grid
            else:
                remaining_grids.append(grid)
        if not remaining_grids:
            if last_won_grid is None:
                raise RuntimeError
            return get_grid_score(last_won_grid, number)
        grids = remaining_grids
    raise RuntimeError


if __name__ == "__main__":
    result = main2()
    print(result)
