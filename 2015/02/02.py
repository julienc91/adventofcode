from collections.abc import Iterator


def parse_input() -> Iterator[tuple[int, int, int]]:
    try:
        while line := input().strip():
            a, b, c = sorted(map(int, line.split("x")))
            yield a, b, c
    except EOFError:
        pass


def main1() -> int:
    res = 0
    for a, b, c in parse_input():
        res += 2 * a * b + 2 * b * c + 2 * a * c + a * b
    return res


def main2() -> int:
    res = 0
    for a, b, c in parse_input():
        res += 2 * a + 2 * b + a * b * c
    return res
