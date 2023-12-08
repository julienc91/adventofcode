import itertools
import math
import re

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
    start: str, end_regex: str, pattern: str, mapping: dict[str, tuple[str, str]]
):
    position = start
    count = 0
    pattern_it = itertools.cycle(pattern)
    while not re.match(end_regex, position):
        direction = 0 if next(pattern_it) == "L" else 1
        position = mapping[position][direction]
        count += 1
    return count


def main1() -> int:
    pattern, mapping = parse_data()
    return count_steps("AAA", "ZZZ", pattern, mapping)


def main2() -> int:
    pattern, mapping = parse_data()
    step_counts = [
        count_steps(start, r"[A-Z]{2}Z", pattern, mapping)
        for start in mapping
        if start.endswith("A")
    ]
    return math.lcm(*step_counts)
