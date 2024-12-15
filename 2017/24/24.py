from collections import defaultdict
from collections.abc import Callable

from utils.parsing import parse_input

Connector = tuple[int, int]


def parse_connectors() -> dict[int, set[Connector]]:
    res = defaultdict(set)
    for line in parse_input():
        a, b = map(int, line.split("/"))
        a, b = min(a, b), max(a, b)
        res[a].add((a, b))
        res[b].add((a, b))
    return res


def _main(sort_key: Callable[[tuple[int, int]], int | tuple[int, int]]) -> int:
    connectors = parse_connectors()

    def inner(bridge: list[Connector], score: tuple[int, int]) -> tuple[int, int]:
        left = bridge[-1][1]
        strength, length = score

        for connector in list(connectors[left]):
            a, b = connector
            right = a if b == left else b

            connectors[a].discard(connector)
            connectors[b].discard(connector)

            score = max(
                inner(bridge + [(left, right)], (strength + left + right, length + 1)),
                score,
                key=sort_key,
            )

            connectors[a].add(connector)
            connectors[b].add(connector)
        return score

    return inner([(0, 0)], (0, 0))[0]


def main1() -> int:
    return _main(lambda score: score[0])


def main2() -> int:
    return _main(lambda score: (score[1], score[0]))
