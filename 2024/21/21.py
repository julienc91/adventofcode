import heapq
from collections.abc import Iterator
from functools import cache
from typing import Literal

from utils.enums import Direction
from utils.parsing import parse_input


def build_map(keyboard: list[str]) -> dict[str, tuple[int, int]]:
    return {
        keyboard[y][x]: (x, y)
        for y in range(len(keyboard))
        for x in range(len(keyboard[y]))
        if keyboard[y][x] != " "
    }


KEYBOARDS_BY_ID = {
    "N": build_map(["789", "456", "123", " 0A"]),
    "D": build_map([" ^A", "<v>"]),
}
REVERSE_KEYBOARDS_BY_ID = {
    "N": {v: k for k, v in KEYBOARDS_BY_ID["N"].items()},
    "D": {v: k for k, v in KEYBOARDS_BY_ID["D"].items()},
}
DIRECTION_TO_SYMBOL = {
    Direction.TOP: "^",
    Direction.RIGHT: ">",
    Direction.BOTTOM: "v",
    Direction.LEFT: "<",
}


def _get_shortest_paths_between_buttons(
    keyboard_id: Literal["N", "D"], start: str, finish: str
) -> Iterator[str]:
    keyboard = KEYBOARDS_BY_ID[keyboard_id]
    reverse_keyboard = REVERSE_KEYBOARDS_BY_ID[keyboard_id]
    queue = [(0, start, "", {start})]
    min_cost = float("inf")

    while queue:
        cost, current, path, visited = heapq.heappop(queue)
        if cost > min_cost:
            break

        if current == finish:
            min_cost = cost
            yield path
            continue

        x, y = keyboard[current]
        for direction in Direction:
            x2, y2 = direction.move(x, y)
            if (x2, y2) not in reverse_keyboard:
                continue

            node = reverse_keyboard[(x2, y2)]
            if node in visited:
                continue

            heapq.heappush(
                queue,
                (
                    cost + 1,
                    node,
                    path + DIRECTION_TO_SYMBOL[direction],
                    visited | {node},
                ),
            )


@cache
def _get_command_length(buttons: tuple[str, ...], depth: int) -> int:
    if depth == 0:
        return len(buttons)

    res = 0
    start = "A"
    for button in buttons:
        paths = _get_shortest_paths_between_buttons("D", start, button)
        res += min(_get_command_length(path + "A", depth - 1) for path in paths)
        start = button
    return res


def get_move_length(start: str, end: str, depth: int) -> int:
    paths = list(_get_shortest_paths_between_buttons("N", start, end))
    return min(_get_command_length(path + "A", depth) for path in paths)


def _main(depth: int) -> int:
    res = 0
    for code in parse_input():
        count = 0
        start = "A"
        for button in code:
            count += get_move_length(start, button, depth)
            start = button
        res += count * int(code[:-1])
    return res


def main1() -> int:
    return _main(2)


def main2() -> int:
    return _main(25)
