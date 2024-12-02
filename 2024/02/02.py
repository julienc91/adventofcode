import itertools
from collections.abc import Iterator

from utils.parsing import parse_input


def parse_reports() -> Iterator[list[int]]:
    for line in parse_input():
        yield list(map(int, line.split()))


def sort_report(report: list[int]) -> list[int]:
    """
    Either return the report untouched or reverse it, so that the
    returned list always is in an "ascending" tendency.
    """
    count_ascending, count_descending = 0, 0
    for a, b in itertools.pairwise(report):
        if a < b:
            count_ascending += 1
        elif b < a:
            count_descending += 1

    if count_descending > count_ascending:
        report = report[::-1]
    return report


def is_safe(report: list[int], allow_error: bool) -> bool:
    def inner(left: list[int], right: list[int], allow_error_: bool = False) -> bool:
        match right:
            case [a, b, *r] if 0 < b - a <= 3:
                return inner([*left, a], [b, *r], allow_error_)
            case [a, b, *r]:
                if not allow_error_:
                    return False
                return inner(left, [a, *r]) or (
                    inner(left[:-1], [*left[-1:], b]) and inner(left, [b, *r])
                )
            case _:
                return True

    return inner([], report, allow_error)


def _main(allow_error: bool) -> int:
    count = 0
    for report in parse_reports():
        report = sort_report(report)
        if is_safe(report, allow_error=allow_error):
            count += 1
    return count


def main1() -> int:
    return _main(False)


def main2() -> int:
    return _main(True)
