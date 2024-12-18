import heapq
from collections.abc import Callable, Iterator, Sequence


def get_shortest_path[Cell](
    start: Cell,
    get_neighbours: Callable[[Cell, int], Iterator[tuple[int, Cell]]],
    is_over: Callable[[Cell], bool],
) -> tuple[int, Sequence[Cell]]:
    queue = [(0, start, [start])]
    visited: set[Cell] = {start}

    while queue:
        weight, cell, path = heapq.heappop(queue)
        if is_over(cell):
            return weight, path

        for next_weight, next_cell in get_neighbours(cell, weight):
            if next_cell in visited:
                continue

            visited.add(next_cell)
            heapq.heappush(queue, (next_weight, next_cell, path + [next_cell]))
    raise RuntimeError("Could not find a path")
