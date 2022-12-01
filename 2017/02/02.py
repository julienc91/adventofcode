import itertools
from collections.abc import Iterator


def parse_input() -> Iterator[list[int]]:
    try:
        while line := input():
            yield [int(x) for x in line.split()]
    except EOFError:
        pass


def main1() -> int:
    res = 0
    for line in parse_input():
        a, b = min(line), max(line)
        res += b - a
    return res


def main2() -> int:
    res = 0
    for line in parse_input():
        for a, b in itertools.permutations(line, 2):
            if a % b == 0:
                res += a // b
                break
    return res
