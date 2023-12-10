from enum import Enum


class Direction(Enum):
    TOP = "top"
    RIGHT = "right"
    BOTTOM = "bottom"
    LEFT = "left"

    @property
    def opposite(self) -> "Direction":
        return {
            Direction.TOP: Direction.BOTTOM,
            Direction.RIGHT: Direction.LEFT,
            Direction.BOTTOM: Direction.TOP,
            Direction.LEFT: Direction.RIGHT,
        }[self]

    def move(self, x: int, y: int) -> tuple[int, int]:
        return {
            Direction.TOP: (x, y - 1),
            Direction.RIGHT: (x + 1, y),
            Direction.BOTTOM: (x, y + 1),
            Direction.LEFT: (x - 1, y),
        }[self]
