from collections.abc import Iterator

from utils.parsing import parse_input

Coordinate = tuple[int, int, int, int]
Grid = list[list[str]]


class GuardPathGenerator:
    def __init__(
        self, grid: Grid, start: Coordinate, visited: set[Coordinate] | None = None
    ):
        self.grid = grid
        self.start = start
        self.visited = visited or set()
        self._is_infinite_loop = None

    def __iter__(self) -> Iterator[Coordinate]:
        yield self.start
        self.visited.add(self.start)

        x, y, dx, dy = self.start
        while True:
            x2, y2 = x + dx, y + dy
            if (x2, y2, dx, dy) in self.visited:
                self._is_infinite_loop = True
                break

            if x2 < 0 or y2 < 0:
                self._is_infinite_loop = False
                break

            try:
                value = self.grid[y2][x2]
            except IndexError:
                self._is_infinite_loop = False
                break

            if value != ".":
                dx, dy = -dy, dx
                continue

            x, y = x2, y2
            yield x, y, dx, dy
            self.visited.add((x, y, dx, dy))

    @property
    def is_infinite_loop(self) -> bool:
        for _ in self:
            pass
        if self._is_infinite_loop is None:
            raise RuntimeError()
        return self._is_infinite_loop


def parse_grid() -> tuple[Grid, Coordinate]:
    grid = []
    guard_position = (-1, -1, 0, 0)
    for line in parse_input():
        if "^" in line:
            guard_position = (line.index("^"), len(grid), 0, -1)
            line = line.replace("^", ".")
        grid.append(list(line))
    return grid, guard_position


def main1() -> int:
    grid, start = parse_grid()
    return len({(x, y) for x, y, _, _ in GuardPathGenerator(grid, start)})


def main2() -> int:
    grid, start = parse_grid()
    valid_obstacles = set()

    cur_pos = None
    visited = {start}
    visited_cells = {(x, y) for x, y, _, _ in visited}

    for next_pos in GuardPathGenerator(grid, start):
        if cur_pos is not None:
            x, y, _, _ = next_pos
            if (x, y) in valid_obstacles or (x, y) in visited_cells:
                continue

            grid[y][x] = "#"
            generator = GuardPathGenerator(grid, cur_pos, visited=set(visited))
            if generator.is_infinite_loop:
                valid_obstacles.add((x, y))
            grid[y][x] = "."

            visited.add(next_pos)
            visited_cells.add((x, y))

        cur_pos = next_pos
    return len(valid_obstacles)
