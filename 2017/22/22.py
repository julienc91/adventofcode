from collections import defaultdict
from collections.abc import Callable
from enum import IntEnum

from utils.enums import Direction
from utils.parsing import parse_input


class State(IntEnum):
    CLEAN = 0
    INFECTED = 1
    WEAKENED = 2
    FLAGGED = 3


def parse_grid() -> tuple[dict[tuple[int, int], State], tuple[int, int]]:
    grid = defaultdict(lambda: State.CLEAN)
    x, y = 0, 0
    for y, line in enumerate(parse_input()):
        for x, c in enumerate(line):
            if c == "#":
                grid[(x, y)] = State.INFECTED
    return grid, (x // 2, y // 2)


def _main(
    nb_ticks: int,
    direction_transition: dict[State, Callable[[Direction], Direction]],
    state_transition: dict[State, State],
) -> int:
    grid, position = parse_grid()
    direction = Direction.TOP
    count = 0
    for _ in range(nb_ticks):
        state = grid[position]
        direction = direction_transition[state](direction)
        state = state_transition[state]
        if state == State.INFECTED:
            count += 1
        grid[position] = state
        position = direction.move(*position)
    return count


def main1() -> int:
    return _main(
        10_000,
        direction_transition={
            State.CLEAN: lambda direction: direction.turn_left(),
            State.INFECTED: lambda direction: direction.turn_right(),
        },
        state_transition={
            State.CLEAN: State.INFECTED,
            State.INFECTED: State.CLEAN,
        },
    )


def main2() -> int:
    return _main(
        10_000_000,
        direction_transition={
            State.CLEAN: lambda direction: direction.turn_left(),
            State.WEAKENED: lambda direction: direction,
            State.INFECTED: lambda direction: direction.turn_right(),
            State.FLAGGED: lambda direction: direction.opposite,
        },
        state_transition={
            State.CLEAN: State.WEAKENED,
            State.WEAKENED: State.INFECTED,
            State.INFECTED: State.FLAGGED,
            State.FLAGGED: State.CLEAN,
        },
    )
