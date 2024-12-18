from collections.abc import Iterator
from functools import cache
from typing import NamedTuple

from utils.enums import Direction
from utils.graph import get_shortest_path
from utils.parsing import parse_input


class State(NamedTuple):
    position: tuple[int, int]
    direction: Direction
    straight_count: int


class Crucible:
    max_straight_count = 3
    min_straight_count = 0

    @classmethod
    @cache
    def _get_next_directions(
        cls, direction: Direction, straight_count: int
    ) -> list[Direction]:
        if straight_count < cls.min_straight_count:
            directions = [direction]
        else:
            directions = [
                direction_
                for direction_ in Direction
                if direction_ != direction.opposite
            ]
            if straight_count >= cls.max_straight_count:
                directions.remove(direction)
        return directions

    @classmethod
    def get_next_states(cls, state: State) -> Iterator[State]:
        if state.position == (0, 0):
            directions = [Direction.RIGHT, Direction.BOTTOM]
        else:
            directions = cls._get_next_directions(state.direction, state.straight_count)
        for direction in directions:
            straight_count = (
                1 if direction != state.direction else (state.straight_count + 1)
            )
            position = (x, y) = direction.move(*state.position)
            if x < 0 or y < 0:
                continue
            yield State(position, direction, straight_count)

    @classmethod
    def can_be_final_state(cls, state: State) -> bool:
        return state.straight_count >= cls.min_straight_count


class UltraCrucible(Crucible):
    min_straight_count = 4
    max_straight_count = 10


def _main(crucible_klass: type[Crucible]) -> int:
    grid = list(list(map(int, line)) for line in parse_input())
    end = (len(grid[-1]) - 1, len(grid) - 1)

    def get_neighbours(state: State, distance: int) -> Iterator[tuple[int, State]]:
        for next_state in crucible_klass.get_next_states(state):
            x, y = next_state.position

            try:
                value = grid[y][x]
            except IndexError:
                continue

            yield distance + value, next_state

    weight, _ = get_shortest_path(
        State((0, 0), Direction.RIGHT, 0),
        get_neighbours=get_neighbours,
        is_over=(
            lambda state: state.position == end
            and crucible_klass.can_be_final_state(state)
        ),
    )
    return weight


def main1() -> int:
    return _main(Crucible)


def main2() -> int:
    return _main(UltraCrucible)
