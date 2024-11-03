import math
import re
from typing import NamedTuple

from utils.parsing import parse_input


class Part(NamedTuple):
    x: int
    m: int
    a: int
    s: int


def parse_workflows() -> dict[str, list[str]]:
    workflows = {}
    for line in parse_input():
        if not line:
            break

        name, rest = line.split("{")
        rules = rest[:-1].split(",")
        workflows[name] = rules
    return workflows


def parse_parts() -> list[Part]:
    parts = []
    for line in parse_input():
        x, m, a, s = map(int, re.findall(r"\d+", line))
        parts.append(Part(x, m, a, s))
    return parts


def apply_workflows(part: Part, workflows: dict[str, list[str]]):
    workflow_name = "in"
    while True:
        rules = workflows[workflow_name]
        for rule in rules:
            outcome = None
            if match := re.fullmatch(r"([xmas])>(\d+):(\w+)", rule):
                values = match.groups()
                if getattr(part, values[0]) > int(values[1]):
                    outcome = values[2]
            elif match := re.fullmatch(r"([xmas])<(\d+):(\w+)", rule):
                values = match.groups()
                if getattr(part, values[0]) < int(values[1]):
                    outcome = values[2]
            elif re.fullmatch(r"\w+", rule):
                outcome = rule
            else:
                raise ValueError(f"Unexpected rule {rule}")

            if outcome == "A":
                return True
            elif outcome == "R":
                return False
            elif outcome is not None:
                workflow_name = outcome
                break
        else:
            raise RuntimeError()


def main1() -> int:
    workflows = parse_workflows()
    parts = parse_parts()

    res = 0
    for part in parts:
        accepted = apply_workflows(part, workflows)
        if accepted:
            res += sum(part)
    return res


def _count_ranges(ranges: dict[str, range]) -> int:
    return math.prod(len(range_) for range_ in ranges.values())


def count_accepted(workflows: dict[str, list[str]]) -> int:
    def inner(workflow_name, ranges) -> int:
        rules = list(workflows[workflow_name])
        total = 0
        while rules:
            rule = rules.pop(0)
            if rule == "R":
                break
            elif rule == "A":
                total += _count_ranges(ranges)
                break
            elif ":" not in rule:
                total += inner(rule, {**ranges})
                break

            match = re.fullmatch(r"([xmas])([<>])(\d+):(\w+)", rule)
            if not match:
                raise ValueError(f"Unexpected rule {rule}")

            category, operator, value, outcome = match.groups()
            range_ = ranges[category]
            value = int(value)
            if operator == ">":
                condition_range = range(max(range_.start, value + 1), range_.stop)
                remaining_range = range(range_.start, min(range_.stop, value + 1))
            else:
                condition_range = range(range_.start, min(range_.stop, value))
                remaining_range = range(max(range_.start, value), range_.stop)

            if outcome == "A":
                accepted_ranges = {**ranges, category: condition_range}
                total += _count_ranges(accepted_ranges)
            elif outcome != "R":
                recursive_ranges = {**ranges, category: condition_range}
                total += inner(outcome, recursive_ranges)
            ranges[category] = remaining_range

        return total

    return inner("in", {c: range(1, 4001) for c in "xmas"})


def main2() -> int:
    workflows = parse_workflows()
    return count_accepted(workflows)
