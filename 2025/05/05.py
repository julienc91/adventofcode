from collections.abc import Iterator

from utils.parsing import parse_input


def parse_ranges() -> list[range]:
    res = []
    for line in parse_input():
        if not line:
            break

        a, b = map(int, line.split("-"))
        res.append(range(a, b + 1))
    return res


def parse_ingredients() -> Iterator[int]:
    yield from parse_input(int)


def main1() -> int:
    count = 0
    ranges = parse_ranges()
    for ingredient in parse_ingredients():
        for r in ranges:
            if ingredient in r:
                count += 1
                break
    return count


def merge_ranges(ranges: list[range]) -> list[range]:
    res = []
    ranges.sort(key=lambda o: o.start)
    for i, r in enumerate(ranges):
        if res and res[-1].stop >= r.stop:
            continue

        a, b = r.start, r.stop
        for r2 in ranges[i + 1 :]:
            if r2.start <= b:
                b = max(b, r2.stop)
        res.append(range(a, b))
    return res


def main2() -> int:
    ranges = parse_ranges()
    ranges = merge_ranges(ranges)
    return sum(len(r) for r in ranges)
