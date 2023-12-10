from collections.abc import Iterator

from utils.enums import Direction


def iterate_spiral() -> Iterator[tuple[int, int]]:
    x, y = 0, 0
    spiral_number = 1
    direction = Direction.RIGHT

    while True:
        yield x, y

        match direction:
            case Direction.RIGHT:
                x += 1
                if x == spiral_number:
                    direction = Direction.TOP
            case Direction.TOP:
                y += 1
                if y == spiral_number:
                    direction = Direction.LEFT
            case Direction.LEFT:
                x -= 1
                if x == -spiral_number:
                    direction = Direction.BOTTOM
            case Direction.BOTTOM:
                y -= 1
                if y == -spiral_number:
                    direction = Direction.RIGHT
                    spiral_number += 1
            case _:
                raise ValueError()


def main1() -> int:
    target = int(input())
    for counter, (x, y) in enumerate(iterate_spiral(), start=1):
        if counter >= target:
            return abs(x) + abs(y)
    raise RuntimeError()


def main2() -> int:
    target = int(input())
    mapping: dict[tuple[int, int], int] = {(0, 0): 1}

    for x, y in iterate_spiral():
        value = sum(
            mapping.get((x + a, y + b), 0) for a in (-1, 0, 1) for b in (-1, 0, 1)
        )
        if value >= target:
            return value

        mapping[(x, y)] = value
    raise RuntimeError()
