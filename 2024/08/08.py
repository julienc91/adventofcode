import itertools
from collections import defaultdict
from fractions import Fraction

from utils.parsing import parse_input


def parse_grid() -> tuple[dict[str, list[tuple[int, int]]], tuple[int, int]]:
    res = defaultdict(list)
    w, h = 0, 0
    for y, line in enumerate(parse_input()):
        h = y + 1
        for x, c in enumerate(line):
            w = x + 1
            if c == ".":
                continue
            res[c].append((x, y))
    return res, (w, h)


def main1() -> int:
    antinode_locations = set()
    grid, (w, h) = parse_grid()
    for frequency, antennas in grid.items():
        for (x1, y1), (x2, y2) in itertools.combinations(antennas, 2):
            candidates = [
                (x1 - (x2 - x1), y1 - (y2 - y1)),
                (x2 + (x2 - x1), y2 + (y2 - y1)),
            ]
            for x3, y3 in candidates:
                if 0 <= x3 < w and 0 <= y3 < h:
                    antinode_locations.add((x3, y3))

    return len(antinode_locations)


def main2() -> int:
    antinode_locations = set()
    grid, (w, h) = parse_grid()
    for frequency, antennas in grid.items():
        for (x1, y1), (x2, y2) in itertools.combinations(antennas, 2):
            antinode_locations |= {(x1, y1), (x2, y2)}
            slope = Fraction(x2 - x1, y2 - y1)
            dx, dy = slope.numerator, slope.denominator

            for increment in (-1, 1):
                k = increment
                while 0 <= (x3 := x1 + k * dx) < w and 0 <= (y3 := y1 + k * dy) < h:
                    antinode_locations.add((x3, y3))
                    k += increment

    return len(antinode_locations)
