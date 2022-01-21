from typing import Callable, Iterator


def _main(parse_lengths: Callable[[], Iterator[tuple[int, int, int]]]) -> int:
    count = 0
    for lengths in parse_lengths():
        a, b, c = sorted(lengths)
        if a + b > c:
            count += 1
    return count


def main1() -> int:
    def parse_lengths() -> Iterator[tuple[int, int, int]]:
        try:
            while line := input().strip():
                a, b, c = map(int, line.split())
                yield a, b, c
        except EOFError:
            pass

    return _main(parse_lengths)


def main2() -> int:
    def parse_lengths() -> Iterator[tuple[int, int, int]]:
        rows: list[list[int]] = [[], [], []]
        try:
            while line := input().strip():
                numbers = map(int, line.split())
                for i, row in zip(numbers, rows):
                    row.append(i)
        except EOFError:
            pass
        for row in rows:
            while row:
                a, b, c = row.pop(0), row.pop(0), row.pop(0)
                yield a, b, c

    return _main(parse_lengths)
