from functools import cache

from utils.parsing import parse_input


@cache
def solve(representation: str, counts: tuple[int, ...]) -> int:
    representation = representation.strip(".")
    if not representation:
        return 0 if counts else 1
    elif not counts:
        return 0 if "#" in representation else 1

    if representation.startswith("#"):
        count = counts[0]
        cut = representation[:count]
        if (len(cut) != count) or ("." in cut):
            return 0

        representation = representation[count:]
        if not representation:
            return len(counts) == 1
        elif representation[0] == "#":
            return 0

        return solve(representation[1:], counts[1:])

    elif representation.endswith("#"):
        return solve(representation[::-1], counts[::-1])

    return solve(representation[1:], counts) + solve("#" + representation[1:], counts)


def _main(factor: int) -> int:
    res = 0
    for line in parse_input():
        left, right = line.split()
        left = "?".join(left for _ in range(factor))
        counts = tuple(map(int, right.split(","))) * factor
        subres = solve(left, counts)
        res += subres
    return res


def main1() -> int:
    return _main(1)


def main2() -> int:
    return _main(5)
