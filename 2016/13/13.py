from collections import deque

Point = tuple[int, int]


def is_valid(x: int, y: int, magic_number: int) -> bool:
    if x < 0 or y < 0:
        return False
    res = x * x + 3 * x + 2 * x * y + y + y * y + magic_number
    return bin(res).count("1") % 2 == 0


def get_neighbours(x: int, y: int, magic_number: int) -> list[Point]:
    neighbours = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    return [(x, y) for (x, y) in neighbours if is_valid(x, y, magic_number)]


def main1() -> int:
    magic_number = int(input())
    target = (31, 39)
    pos = (1, 1)

    visited: set[Point] = set()
    stack: deque[tuple[Point, set[Point], int]] = deque([(pos, visited, 0)])

    while stack:
        pos, visited, steps = stack.popleft()
        if pos == target:
            return steps

        new_visited = visited | {pos}
        for new_pos in get_neighbours(*pos, magic_number):
            if new_pos in new_visited:
                continue
            stack.append((new_pos, new_visited, steps + 1))

    raise RuntimeError("No path found")


def main2() -> int:
    magic_number = int(input())
    pos = (1, 1)
    visited: set[Point] = {pos}
    all_visited: set[Point] = {pos}
    stack: deque[tuple[Point, set[Point], int]] = deque([(pos, visited, 0)])
    while stack:
        pos, visited, steps = stack.popleft()
        if steps >= 50:
            continue

        new_visited = visited | {pos}
        for new_pos in get_neighbours(*pos, magic_number):
            if new_pos in new_visited:
                continue
            all_visited.add(new_pos)
            stack.append((new_pos, new_visited, steps + 1))
    return len(all_visited)
