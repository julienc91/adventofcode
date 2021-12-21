import itertools
from collections import defaultdict


def parse_affinities() -> dict[str, dict[str, int]]:
    res: dict[str, dict[str, int]] = defaultdict(dict)
    try:
        while line := input().strip():
            a, _, lose_or_gain, quantity, _, _, _, _, _, _, b = line.rstrip(".").split()
            res[a][b] = int(quantity) * (1 if lose_or_gain == "gain" else -1)
    except EOFError:
        pass
    return res


def evaluate(stack: list[str], affinities: dict[str, dict[str, int]]) -> int:
    score = 0
    for a, b, c in zip(stack, stack[1:] + stack[:1], stack[2:] + stack[:2]):
        score += affinities[b].get(a, 0) + affinities[b].get(c, 0)
    return score


def _main(affinities: dict[str, dict[str, int]]) -> int:
    res = 0
    names = list(affinities.keys())
    reference = names.pop()
    for perm in itertools.permutations(names):
        stack = [reference, *perm]
        res = max(res, evaluate(stack, affinities))
    return res


def main1() -> int:
    affinities = parse_affinities()
    return _main(affinities)


def main2() -> int:
    affinities = parse_affinities()
    affinities["me"] = {}
    return _main(affinities)
