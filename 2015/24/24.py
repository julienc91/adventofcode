import itertools
import math
from typing import Iterator


def parse_weights() -> list[int]:
    res: list[int] = []
    try:
        while line := input().strip():
            res.append(int(line))
    except EOFError:
        pass
    return res


def get_groups_of_weight(weights: list[int], target: int) -> Iterator[tuple[int, ...]]:
    for group_size in range(len(weights)):
        for group in itertools.combinations(weights, group_size):
            total = sum(group)
            if total != target:
                continue
            yield group


def validate_grouping(weights: list[int], target: int, nb_groups: int) -> bool:
    if nb_groups <= 0:
        return len(weights) == 0
    if nb_groups == 1:
        return sum(weights) == target

    for group in get_groups_of_weight(weights, target):
        remaining_weights = [w for w in weights if w not in group]
        if validate_grouping(remaining_weights, target, nb_groups - 1):
            return True
    return False


def _main(nb_groups: int) -> int:
    weights = parse_weights()
    total = sum(weights)
    assert total % nb_groups == 0
    target = total // nb_groups

    min_product = math.prod(weights)
    min_weights = len(weights)

    for group in get_groups_of_weight(weights, target):
        if len(group) > min_weights:
            break

        product = math.prod(group)
        if product > min_product:
            continue

        remaining_weights = [w for w in weights if w not in group]
        if validate_grouping(remaining_weights, target, nb_groups - 1):
            min_weights = len(group)
            min_product = min(min_product, product)

    return min_product


def main1() -> int:
    return _main(nb_groups=3)


def main2() -> int:
    return _main(nb_groups=4)
