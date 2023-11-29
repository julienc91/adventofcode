from collections.abc import Callable

from utils.parsing import parse_input


def _main(checker: Callable[[tuple[int, int], tuple[int, int]], bool]) -> int:
    count = 0
    for line in parse_input():
        range1, range2 = line.split(",")
        a1, a2 = map(int, range1.split("-"))
        b1, b2 = map(int, range2.split("-"))
        if checker((a1, a2), (b1, b2)):
            count += 1
    return count


def main1() -> int:
    return _main(
        lambda a, b: a[0] <= b[0] and a[1] >= b[1] or b[0] <= a[0] and b[1] >= a[1]
    )


def main2() -> int:
    return _main(lambda a, b: len(range(max(a[0], b[0]), min(a[1], b[1]) + 1)) > 0)
