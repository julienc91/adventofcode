import itertools
import math
import re
from collections.abc import Iterator

from utils.parsing import parse_input


def parse_data() -> tuple[str, dict[str, tuple[str, str]]]:
    pattern = input()
    input()

    mapping = {}
    for line in parse_input():
        start, left, right = re.findall(r"\w+", line)
        mapping[start] = (left, right)
    return pattern, mapping


def count_steps(
    start: str,
    end_regex: str,
    pattern: Iterator[str],
    mapping: dict[str, tuple[str, str]],
) -> tuple[int, str]:
    position = start
    count = 0
    while count == 0 or not re.match(end_regex, position):
        direction = 0 if next(pattern) == "L" else 1
        position = mapping[position][direction]
        count += 1
    return count, position


def main1() -> int:
    pattern, mapping = parse_data()
    count, _ = count_steps("AAA", "ZZZ", itertools.cycle(pattern), mapping)
    return count


def assume_lcm_hypothesis(
    start: str, pattern: str, mapping: dict[str, tuple[str, str]]
) -> int:
    pattern_it = itertools.cycle(pattern)
    count, finish = count_steps(start, r"[A-Z]{2}Z", pattern_it, mapping)
    if count % len(pattern) != 0:
        raise ValueError("LCM hypothesis is not correct")

    new_count, new_finish = count_steps(finish, r"[A-Z]{2}Z", pattern_it, mapping)
    if (new_count, new_finish) != (count, finish):
        raise ValueError("LCM hypothesis is not correct")
    return count


def main2() -> int:
    pattern, mapping = parse_data()
    step_counts = [
        assume_lcm_hypothesis(start, pattern, mapping)
        for start in mapping
        if start.endswith("A")
    ]
    return math.lcm(*step_counts)
