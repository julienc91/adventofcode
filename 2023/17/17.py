import heapq
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Self

from utils.enums import Direction
from utils.parsing import parse_input


@dataclass(frozen=True)
class Crucible:
    position: tuple[int, int]
    direction: Direction
    straight_count: int = -1

    def _get_next_directions(self) -> list[Direction]:
        if self.position == (0, 0):
            return [Direction.RIGHT, Direction.BOTTOM]

        directions = [
            direction for direction in Direction if direction != self.direction.opposite
        ]
        if self.straight_count >= 2:
            directions.remove(self.direction)
        return directions

    @classmethod
    def get_next_states(cls, state: Self) -> Iterator[Self]:
        for direction in state._get_next_directions():
            straight_count = (
                0 if direction != state.direction else (state.straight_count + 1)
            )
            position = (x, y) = direction.move(*state.position)
            if x < 0 or y < 0:
                continue
            yield cls(position, direction, straight_count)

    def can_be_final_state(self) -> bool:
        return True

    def __hash__(self) -> int:
        return hash((self.position, self.direction, self.straight_count))

    def __lt__(self, other: Self) -> bool:
        return False


class UltraCrucible(Crucible):
    straight_count: int

    def _get_next_directions(self) -> list[Direction]:
        if self.position == (0, 0):
            return [Direction.RIGHT, Direction.BOTTOM]

        if self.straight_count < 3:
            return [self.direction]

        directions = [
            direction for direction in Direction if direction != self.direction.opposite
        ]
        if self.straight_count >= 9:
            directions.remove(self.direction)
        return directions

    def can_be_final_state(self) -> bool:
        return self.straight_count >= 3


def shortest_path(
    grid,
    start: tuple[int, int],
    end: tuple[int, int],
    crucible_klass: type[Crucible],
):
    state = crucible_klass(start, Direction.RIGHT)
    queue = [(0, state)]
    visited = set()

    while queue:
        distance, state = heapq.heappop(queue)
        for next_state in crucible_klass.get_next_states(state):
            if next_state in visited:
                continue

            visited.add(next_state)
            x, y = next_state.position

            try:
                value = grid[y][x]
            except IndexError:
                continue

            next_distance = distance + value
            if next_state.position == end and next_state.can_be_final_state():
                return distance + value

            heapq.heappush(queue, (next_distance, next_state))

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
