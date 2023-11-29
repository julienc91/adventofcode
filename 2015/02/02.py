from collections.abc import Iterator

from utils.parsing import parse_input


def parse_sizes() -> Iterator[tuple[int, int, int]]:
    for line in parse_input():
        a, b, c = sorted(map(int, line.split("x")))
        yield a, b, c


def main1() -> int:
    res = 0
    for a, b, c in parse_sizes():
        res += 2 * a * b + 2 * b * c + 2 * a * c + a * b
    return res


def main2() -> int:
    res = 0
    for a, b, c in parse_sizes():
        res += 2 * a + 2 * b + a * b * c
    return res
