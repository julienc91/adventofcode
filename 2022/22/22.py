import re
from collections import defaultdict
from collections.abc import Iterator
from enum import Enum


class State(Enum):
    VOID = " "
    WALL = "#"
    OPEN = "."


class Direction(Enum):
    TOP = "^"
    RIGHT = ">"
    BOTTOM = "v"
    LEFT = "<"

    def turn(self, turn: str) -> "Direction":
        directions = list(Direction)
        if turn == "R":
            return directions[(directions.index(self) + 1) % len(directions)]
        elif turn == "L":
            return directions[(directions.index(self) - 1) % len(directions)]
        raise ValueError(turn)

    @property
    def opposite(self) -> "Direction":
        directions = list(Direction)
        return directions[(directions.index(self) + 2) % len(directions)]

    @property
    def score(self) -> int:
        return {
            Direction.RIGHT: 0,
            Direction.BOTTOM: 1,
            Direction.LEFT: 2,
            Direction.TOP: 3,
        }[self]


class AbstractForm:
    @classmethod
    def from_input(cls) -> "AbstractForm":
        raise NotImplementedError

    def apply_instructions(self, instructions: str) -> int:
        raise NotImplementedError


class Grid(AbstractForm):
    def __init__(self) -> None:
        self.grid: dict[tuple[int, int], State] = defaultdict(lambda: State.VOID)
        self.top_bounds: dict[int, int] = {}
        self.right_bounds: dict[int, int] = {}
        self.bottom_bounds: dict[int, int] = {}
        self.left_bounds: dict[int, int] = {}

    @classmethod
    def from_input(cls) -> "Grid":
        grid: "Grid" = Grid()
        y = 0
        while line := input().rstrip():
            grid._add_row(y, [State(c) for c in line])
            y += 1
        return grid

    def _add_row(self, y: int, row: list[State]) -> None:
        for x, c in enumerate(row):
            state = State(c)
            if state == State.VOID:
                continue

            self.grid[(x, y)] = state
            self.top_bounds[x] = (
                min(self.top_bounds[x], y) if x in self.top_bounds else y
            )
            self.right_bounds[y] = (
                max(self.right_bounds[y], x) if y in self.right_bounds else x
            )
            self.bottom_bounds[x] = (
                max(self.top_bounds[x], y) if x in self.bottom_bounds else y
            )
            self.left_bounds[y] = (
                min(self.left_bounds[y], x) if y in self.left_bounds else x
            )

    def _move(
        self, x: int, y: int, direction: Direction, count: int, turn: str
    ) -> tuple[int, int, Direction]:
        if count == 0:
            direction = direction.turn(turn)
            return x, y, direction

        if direction == Direction.TOP:
            x2, y2 = x, y - 1
        elif direction == Direction.RIGHT:
            x2, y2 = x + 1, y
        elif direction == Direction.BOTTOM:
            x2, y2 = x, y + 1
        elif direction == Direction.LEFT:
            x2, y2 = x - 1, y
        else:
            raise ValueError(direction)

        next_cell = self.grid[(x2, y2)]
        if next_cell == State.VOID:
            if direction == Direction.TOP:
                y2 = self.bottom_bounds[x2]
            elif direction == Direction.RIGHT:
                x2 = self.left_bounds[y2]
            elif direction == Direction.BOTTOM:
                y2 = self.top_bounds[x2]
            elif direction == Direction.LEFT:
                x2 = self.right_bounds[y2]
            else:
                raise ValueError(direction)

            next_cell = self.grid[(x2, y2)]

        if next_cell == State.WALL:
            return self._move(x, y, direction, 0, turn)
        elif next_cell == State.OPEN:
            return self._move(x2, y2, direction, count - 1, turn)
        raise RuntimeError("Unexpected void")

    def apply_instructions(self, instructions: str) -> int:
        y = 0
        x = self.left_bounds[y]
        direction = Direction.RIGHT

        for count, turn in iterate_instructions(instructions):
            x, y, direction = self._move(x, y, direction, count, turn)
        return (y + 1) * 1000 + (x + 1) * 4 + direction.score


class Cube(AbstractForm):
    FACE_SIZE = 50

    def __init__(self) -> None:
        self.grid: dict[tuple[int, int], State] = defaultdict(lambda: State.VOID)

    @classmethod
    def from_input(cls) -> "Cube":
        cube = Cube()
        y = 0
        while line := input().rstrip():
            cube._add_row(y, [State(c) for c in line])
            y += 1
        return cube

    def _add_row(self, y: int, row: list[State]) -> None:
        for x, c in enumerate(row):
            state = State(c)
            if state == State.VOID:
                continue
            self.grid[(x, y)] = state

    def _move(
        self, x: int, y: int, direction: Direction, count: int, turn: str
    ) -> tuple[int, int, Direction]:
        if count == 0:
            direction = direction.turn(turn)
            return x, y, direction

        initial_direction = direction
        if direction == Direction.TOP:
            x2, y2 = x, y - 1
        elif direction == Direction.RIGHT:
            x2, y2 = x + 1, y
        elif direction == Direction.BOTTOM:
            x2, y2 = x, y + 1
        elif direction == Direction.LEFT:
            x2, y2 = x - 1, y
        else:
            raise ValueError(direction)

        next_cell = self.grid[(x2, y2)]
        # Hardcoded, fuck it
        if next_cell == State.VOID:
            if direction == Direction.TOP:
                if 0 <= x < self.FACE_SIZE:
                    direction = Direction.RIGHT
                    x2, y2 = self.FACE_SIZE, self.FACE_SIZE + x
                elif self.FACE_SIZE <= x < 2 * self.FACE_SIZE:
                    direction = Direction.RIGHT
                    x2, y2 = 0, 3 * self.FACE_SIZE + x - self.FACE_SIZE
                else:
                    direction = Direction.TOP
                    x2, y2 = x - 2 * self.FACE_SIZE, 4 * self.FACE_SIZE - 1
            elif direction == Direction.BOTTOM:
                if 0 <= x < self.FACE_SIZE:
                    direction = Direction.BOTTOM
                    x2, y2 = 2 * self.FACE_SIZE + x, 0
                elif self.FACE_SIZE <= x < 2 * self.FACE_SIZE:
                    direction = Direction.LEFT
                    x2, y2 = self.FACE_SIZE - 1, 3 * self.FACE_SIZE + x - self.FACE_SIZE
                else:
                    direction = Direction.LEFT
                    x2, y2 = 2 * self.FACE_SIZE - 1, x - self.FACE_SIZE
            elif direction == Direction.RIGHT:
                if 0 <= y < self.FACE_SIZE:
                    direction = Direction.LEFT
                    x2, y2 = 2 * self.FACE_SIZE - 1, 3 * self.FACE_SIZE - 1 - y
                elif self.FACE_SIZE <= y < 2 * self.FACE_SIZE:
                    direction = Direction.TOP
                    x2, y2 = self.FACE_SIZE + y, self.FACE_SIZE - 1
                elif 2 * self.FACE_SIZE <= y < 3 * self.FACE_SIZE:
                    direction = Direction.LEFT
                    x2, y2 = 3 * self.FACE_SIZE - 1, 3 * self.FACE_SIZE - 1 - y
                else:
                    direction = Direction.TOP
                    x2, y2 = y - 2 * self.FACE_SIZE, 3 * self.FACE_SIZE - 1
            elif direction == Direction.LEFT:
                if 0 <= y < self.FACE_SIZE:
                    direction = Direction.RIGHT
                    x2, y2 = 0, 3 * self.FACE_SIZE - 1 - y
                elif self.FACE_SIZE <= y < 2 * self.FACE_SIZE:
                    direction = Direction.BOTTOM
                    x2, y2 = y - self.FACE_SIZE, 2 * self.FACE_SIZE
                elif 2 * self.FACE_SIZE <= y < 3 * self.FACE_SIZE:
                    direction = Direction.RIGHT
                    x2, y2 = self.FACE_SIZE, 3 * self.FACE_SIZE - 1 - y
                else:
                    direction = Direction.BOTTOM
                    x2, y2 = y - 2 * self.FACE_SIZE, 0
            else:
                raise ValueError

            next_cell = self.grid[(x2, y2)]

        if next_cell == State.WALL:
            return self._move(x, y, initial_direction, 0, turn)
        elif next_cell == State.OPEN:
            return self._move(x2, y2, direction, count - 1, turn)
        raise RuntimeError("Unexpected void")

    def apply_instructions(self, instructions: str) -> int:
        x, y = 50, 0
        direction = Direction.RIGHT
        for count, turn in iterate_instructions(instructions):
            x, y, direction = self._move(x, y, direction, count, turn)
        return (y + 1) * 1000 + (x + 1) * 4 + direction.score


def iterate_instructions(raw_instructions: str) -> Iterator[tuple[int, str]]:
    regex = re.compile(r"(\d+[LR])")
    for instruction in regex.findall(raw_instructions):
        number, direction = int(instruction[:-1]), instruction[-1]
        yield number, direction


def parse_input(form_parser: type[AbstractForm]) -> tuple[AbstractForm, str]:
    form = form_parser.from_input()
    instructions = input().strip()
    return form, instructions


def main1() -> int:
    grid, instructions = parse_input(Grid)
    return grid.apply_instructions(instructions)


def main2() -> int:
    cube, instructions = parse_input(Cube)
    return cube.apply_instructions(instructions)
