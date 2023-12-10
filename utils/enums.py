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
