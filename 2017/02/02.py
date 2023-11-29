import itertools
from collections.abc import Iterator

from utils.parsing import parse_input


def parse_spreadsheet() -> Iterator[list[int]]:
    for line in parse_input():
        yield [int(x) for x in line.split()]


def main1() -> int:
    res = 0
    for line in parse_spreadsheet():
        a, b = min(line), max(line)
        res += b - a
    return res


def main2() -> int:
    res = 0
    for line in parse_spreadsheet():
        for a, b in itertools.permutations(line, 2):
            if a % b == 0:
                res += a // b
                break
    return res
