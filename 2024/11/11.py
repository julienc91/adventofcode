from collections import defaultdict
from functools import cache


def parse_stones() -> list[int]:
    return list(map(int, input().split()))


@cache
def iterate_stone(value: int) -> list[int]:
    if value == 0:
        return [1]
    value_str = str(value)
    if len(value_str) % 2 == 0:
        left = int(value_str[: len(value_str) // 2])
        right = int(value_str[len(value_str) // 2 :])
        return [left, right]
    return [value * 2024]


def _main(steps: int) -> int:
    stones = parse_stones()
    stones_by_value = defaultdict(int)
    for stone in stones:
        stones_by_value[stone] += 1

    for _ in range(steps):
        updated_stones_by_value = defaultdict(int)
        for stone, count in stones_by_value.items():
            updated_stones = iterate_stone(stone)
            for updated_stone in updated_stones:
                updated_stones_by_value[updated_stone] += count
        stones_by_value = updated_stones_by_value

    return sum(stones_by_value.values())


def main1() -> int:
    return _main(25)


def main2() -> int:
    return _main(75)
