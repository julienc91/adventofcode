from collections.abc import Callable, Iterator

from utils.parsing import parse_input


def _main(parse_lengths: Callable[[], Iterator[tuple[int, int, int]]]) -> int:
    count = 0
    for lengths in parse_lengths():
        a, b, c = sorted(lengths)
        if a + b > c:
            count += 1
    return count


def main1() -> int:
    def parse_lengths() -> Iterator[tuple[int, int, int]]:
        for line in parse_input():
            a, b, c = map(int, line.split())
            yield a, b, c

    return _main(parse_lengths)


def main2() -> int:
    def parse_lengths() -> Iterator[tuple[int, int, int]]:
        rows: list[list[int]] = [[], [], []]
        for line in parse_input():
            numbers = map(int, line.split())
            for i, row in zip(numbers, rows):
                row.append(i)
        for row in rows:
            while row:
                a, b, c = row.pop(0), row.pop(0), row.pop(0)
                yield a, b, c

    return _main(parse_lengths)
