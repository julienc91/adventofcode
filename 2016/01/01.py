from collections.abc import Iterator
from enum import Enum


class Direction(Enum):
    NORTH = (0, 1)
    EAST = (1, 0)
    SOUTH = (0, -1)
    WEST = (-1, 0)

    def turn_right(self) -> "Direction":
        x, y = self.value
        return Direction((y, -x))

    def turn_left(self) -> "Direction":
        x, y = self.value
        return Direction((-y, x))


def parse_instructions() -> Iterator[tuple["Direction", int]]:
    instructions = input().strip().split(", ")
    direction = Direction.NORTH
    for instruction in instructions:
        turn = instruction[0]
        if turn == "R":
            direction = direction.turn_right()
        else:
            direction = direction.turn_left()

        count = int(instruction[1:])
        yield direction, count


def main1() -> int:
    x, y = 0, 0
    for direction, count in parse_instructions():
        coeff_x, coeff_y = direction.value
        x += coeff_x * count
        y += coeff_y * count

    return abs(x) + abs(y)


def main2() -> int:
    x, y = 0, 0
    visited = {(x, y)}
    for direction, count in parse_instructions():
        coeff_x, coeff_y = direction.value
        for step in range(count):
            x += coeff_x
            y += coeff_y
            if (x, y) in visited:
                return abs(x) + abs(y)

            visited.add((x, y))
    raise RuntimeError()
