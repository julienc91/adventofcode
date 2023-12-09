from collections.abc import Iterator

from utils.parsing import parse_input


def process_series(series: list[int]) -> int:
    if all(i == 0 for i in series):
        return 0

    sub_res = process_series(
        [series[i + 1] - series[i] for i in range(len(series) - 1)]
    )
    return sub_res + series[-1]


def parse_series() -> Iterator[list[int]]:
    for line in parse_input():
        yield list(map(int, line.split()))


def main1() -> int:
    return sum(process_series(series) for series in parse_series())


def main2() -> int:
    return sum(process_series(series[::-1]) for series in parse_series())
