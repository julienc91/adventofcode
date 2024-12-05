from collections import defaultdict
from collections.abc import Iterator
from functools import cmp_to_key

from utils.parsing import parse_input


def parse_dependencies() -> dict[int, set[int]]:
    dependencies = defaultdict(set)
    for line in parse_input():
        if not line:
            break

        a, b = list(map(int, line.split("|")))
        dependencies[a].add(b)

    return dependencies


def parse_updates() -> Iterator[list[int]]:
    for line in parse_input():
        yield list(map(int, line.split(",")))


def is_update_valid(update: list[int], dependencies: dict[int, set[int]]) -> bool:
    for i, n in enumerate(update):
        if not dependencies[n].isdisjoint(update[:i]):
            return False
    return True


def make_update_valid(
    update: list[int], dependencies: dict[int, set[int]]
) -> list[int]:
    def compare(a: int, b: int) -> int:
        if a in dependencies[b]:
            return -1
        elif b in dependencies[a]:
            return 1
        return 0

    return sorted(update, key=cmp_to_key(compare))


def main1() -> int:
    res = 0
    dependencies = parse_dependencies()
    for update in parse_updates():
        if is_update_valid(update, dependencies):
            res += update[len(update) // 2]
    return res


def main2() -> int:
    res = 0
    dependencies = parse_dependencies()
    for update in parse_updates():
        if is_update_valid(update, dependencies):
            continue

        update = make_update_valid(update, dependencies)
        res += update[len(update) // 2]
    return res
