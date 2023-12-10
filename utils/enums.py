from enum import Enum


class Direction(Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"

    @property
    def opposite(self) -> "Direction":
        if self == Direction.TOP:
            return Direction.BOTTOM
        elif self == Direction.RIGHT:
            return Direction.LEFT
        elif self == Direction.BOTTOM:
            return Direction.TOP
        else:
            return Direction.RIGHT

    def move(self, x: int, y: int) -> tuple[int, int]:
        if self == Direction.TOP:
            return x, y - 1
        elif self == Direction.RIGHT:
            return x + 1, y
        elif self == Direction.BOTTOM:
            return x, y + 1
        else:
            return x - 1, y

    def turn_right(self) -> "Direction":
        if self == Direction.TOP:
            return Direction.RIGHT
        elif self == Direction.RIGHT:
            return Direction.BOTTOM
        elif self == Direction.BOTTOM:
            return Direction.LEFT
        else:
            return Direction.TOP

    def turn_left(self) -> "Direction":
        if self == Direction.TOP:
            return Direction.LEFT
        elif self == Direction.RIGHT:
            return Direction.TOP
        elif self == Direction.BOTTOM:
            return Direction.RIGHT
        else:
            return Direction.BOTTOM
