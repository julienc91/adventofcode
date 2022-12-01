from collections.abc import Callable


def main_(cost: Callable[[int, int], int]) -> int:
    data = [int(i) for i in input().split(",")]
    return min(
        sum(cost(pos, target) for pos in data) for target in range(min(data), max(data))
    )


def main1() -> int:
    return main_(lambda pos, target: abs(pos - target))


def main2() -> int:
    return main_(lambda pos, target: abs(pos - target) * (abs(pos - target) + 1) // 2)
