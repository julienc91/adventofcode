from collections.abc import Iterator
from functools import cache

from utils.parsing import parse_input


def parse_towels() -> tuple[str, ...]:
    return tuple(input().split(", "))


def parse_patterns() -> Iterator[str]:
    input()
    yield from parse_input()


def is_pattern_possible(pattern: str, towels: tuple[str, ...]) -> bool:
    if not pattern:
        return True

    return any(
        pattern.startswith(towel) and is_pattern_possible(pattern[len(towel) :], towels)
        for towel in towels
    )


@cache
def count_possible_patterns(pattern: str, towels: tuple[str, ...]) -> int:
    if not pattern:
        return 1

    count = 0
    for towel in towels:
        if pattern.startswith(towel):
            count += count_possible_patterns(pattern[len(towel) :], towels)
    return count


def main1() -> int:
    count = 0
    towels = parse_towels()
    for pattern in parse_patterns():
        if is_pattern_possible(pattern, towels):
            count += 1
    return count


def main2() -> int:
    count = 0
    towels = parse_towels()
    for pattern in parse_patterns():
        count += count_possible_patterns(pattern, towels)
    return count
