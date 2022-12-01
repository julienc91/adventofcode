import random
import re
from collections import defaultdict
from collections.abc import Iterator


def parse_transformations() -> dict[str, list[str]]:
    res = defaultdict(list)
    while line := input().strip():
        a, b = line.split(" => ")
        res[a].append(b)
    return res


def iter_transformations(formula: str, key: str, value: str) -> Iterator[str]:
    iterator = re.finditer(key, formula)
    for match in iterator:
        yield formula[: match.start()] + value + formula[match.end() :]


def main1() -> int:
    transformations = parse_transformations()
    formula = input().strip()

    res = set()
    for key in transformations:
        for value in transformations[key]:
            for new_formula in iter_transformations(formula, key, value):
                res.add(new_formula)
    return len(res)


def count_transformations(
    formula: str, transformations: dict[str, str], keys: list[str]
) -> int:
    def inner(s: str) -> int:
        if s == "e":
            return 0

        for key in keys:
            if key not in s:
                continue

            new_s = next(iter_transformations(s, key, transformations[key]))
            return 1 + inner(new_s)

        raise KeyError(s)

    while True:
        try:
            return inner(formula)
        except KeyError:
            random.shuffle(keys)


def main2() -> int:
    transformations = parse_transformations()
    reverse_transformations = {}
    for k, v in transformations.items():
        for item in v:
            assert item not in reverse_transformations
            reverse_transformations[item] = k

    formula = input().strip()
    return count_transformations(
        formula, reverse_transformations, list(reverse_transformations.keys())
    )
