from utils.parsing import parse_input


def parse_grid() -> tuple[list[str], tuple[int, int]]:
    grid = []
    guard_position = (-1, -1)
    for line in parse_input():
        if "^" in line:
            guard_position = (line.index("^"), len(grid))
            line = line.replace("^", ".")
        grid.append(line)
    return grid, guard_position


def simulate_guard(
    grid: list[str], x: int, y: int
) -> tuple[set[tuple[int, int]], bool]:
    dx, dy = 0, -1
    positions = {(x, y, dx, dy)}
    infinite_loop = False
    while True:
        x2, y2 = x + dx, y + dy
        if (x2, y2, dx, dy) in positions:
            infinite_loop = True
            break

        if x2 < 0 or y2 < 0 or y2 >= len(grid) or x2 >= len(grid[y2]):
            break

        if grid[y2][x2] == ".":
            x, y = x2, y2
            positions.add((x, y, dx, dy))
            continue

        dx, dy = -dy, dx

    return {(x, y) for x, y, _, _ in positions}, infinite_loop


def main1() -> int:
    grid, (x, y) = parse_grid()
    positions, _ = simulate_guard(grid, x, y)
    return len(positions)


def main2() -> int:
    grid, (x, y) = parse_grid()
    count = 0
    positions, _ = simulate_guard(grid, x, y)
    positions.remove((x, y))
    for i, j in positions:
        initial = grid[j]
        grid[j] = initial[:i] + "#" + initial[i + 1 :]
        _, infinite_loop = simulate_guard(grid, x, y)
        if infinite_loop:
            count += 1
        grid[j] = initial
    return count
