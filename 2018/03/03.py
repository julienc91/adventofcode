import re
from collections import defaultdict

from utils.parsing import parse_input


def parse_squares() -> list[tuple[int, int, int, int, int]]:
    res = []
    for line in parse_input():
        id_, x, y, w, h = map(int, re.findall(r"\d+", line))
        res.append((id_, x, y, w, h))
    return res


def main1() -> int:
    grid = defaultdict(bool)
    squares = parse_squares()
    for _, x0, y0, w, h in squares:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                grid[(x, y)] = (x, y) not in grid

    return sum(1 for value in grid.values() if value is False)


def main2() -> int:
    grid = defaultdict(set)
    squares = parse_squares()
    not_overlapping_square_ids = {s[0] for s in squares}
    for id_, x0, y0, w, h in squares:
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                grid[(x, y)].add(id_)
                if len(grid[(x, y)]) > 1:
                    not_overlapping_square_ids -= grid[(x, y)]

    return not_overlapping_square_ids.pop()
