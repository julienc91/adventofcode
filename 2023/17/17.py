import heapq
from collections import namedtuple
from collections.abc import Iterator
from functools import cache

from utils.enums import Direction
from utils.parsing import parse_input


class State(namedtuple("State", ["position", "direction", "straight_count"])):
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


def shortest_path(
    grid,
    start: tuple[int, int],
    end: tuple[int, int],
    crucible_klass: type[Crucible],
):
    state = State(start, Direction.RIGHT, 0)
    count = 0
    queue: list[tuple[int, int, State]] = [(0, count, state)]
    visited = set()

    while queue:
        distance, _, state = heapq.heappop(queue)
        if state.position == end and crucible_klass.can_be_final_state(state):
            return distance

        for next_state in crucible_klass.get_next_states(state):
            if next_state in visited:
                continue

            visited.add(next_state)
            x, y = next_state.position

            try:
                value = grid[y][x]
            except IndexError:
                continue

            count += 1
            next_distance = distance + value
            heapq.heappush(queue, (next_distance, count, next_state))

    raise RuntimeError()


def _main(crucible_klass: type[Crucible]) -> int:
    grid = list(list(map(int, line)) for line in parse_input())
    return shortest_path(
        grid, (0, 0), (len(grid[-1]) - 1, len(grid) - 1), crucible_klass
    )


def main1() -> int:
    return _main(Crucible)


def main2() -> int:
    return _main(UltraCrucible)
