import re
from collections import defaultdict
from typing import Callable, Iterator

instruction_format = re.compile(
    r"(turn on|turn off|toggle) (\d+),(\d+) through (\d+),(\d+)"
)


def parse_instructions() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def update_grid(
    instruction: str,
    grid: dict[tuple[int, int], int],
    operations: dict[str, Callable[[int], int]],
) -> None:
    match = instruction_format.search(instruction)
    assert match

    x1, y1 = map(int, (match.group(2), match.group(3)))
    x2, y2 = map(int, (match.group(4), match.group(5)))
    operator = operations[match.group(1)]

    for x in range(x1, x2 + 1):
        for y in range(y1, y2 + 1):
            grid[(x, y)] = operator(grid[(x, y)])


def main_(operations: dict[str, Callable[[int], int]]) -> int:
    grid: dict[tuple[int, int], int] = defaultdict(int)
    for instruction in parse_instructions():
        update_grid(instruction, grid, operations)
    return sum(grid.values())


def main1() -> int:
    operations = {
        "turn on": lambda _: 1,
        "turn off": lambda _: 0,
        "toggle": lambda v: (v + 1) % 2,
    }
    return main_(operations)


def main2() -> int:
    operations = {
        "turn on": lambda v: v + 1,
        "turn off": lambda v: max(v - 1, 0),
        "toggle": lambda v: v + 2,
    }
    return main_(operations)
