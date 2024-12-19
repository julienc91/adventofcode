import itertools
from collections.abc import Iterator

from utils.parsing import parse_input


def parse_changes() -> Iterator[int]:
    yield from parse_input(int)


def main1() -> int:
    return sum(parse_changes())


def main2() -> int:
    seen = {0}
    count = 0
    for change in itertools.cycle(parse_changes()):
        count += change
        if count in seen:
            return count
        seen.add(count)
    return -1
