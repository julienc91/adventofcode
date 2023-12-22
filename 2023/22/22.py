import itertools
import re
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass, field
from functools import cache

from utils.parsing import parse_input


@dataclass
class Brick:
    id: int
    x1: int
    y1: int
    z1: int
    x2: int
    y2: int
    z2: int

    floating: bool = True
    supported_by: set["Brick"] = field(default_factory=set)
    supporting: set["Brick"] = field(default_factory=set)

    def __hash__(self):
        return hash(("brick", self.id))

    def move_down(self) -> None:
        self.z1 -= 1
        self.z2 -= 1

    def get_surface(self) -> Iterator[tuple[int, int]]:
        return itertools.product(
            range(self.x1, self.x2 + 1),
            range(self.y1, self.y2 + 1),
        )

    def get_volume(self) -> Iterator[tuple[int, int, int]]:
        return itertools.product(
            range(self.x1, self.x2 + 1),
            range(self.y1, self.y2 + 1),
            range(self.z1, self.z2 + 1),
        )


def parse_bricks() -> Iterator[Brick]:
    for i, line in enumerate(parse_input(), start=1):
        x1, y1, z1, x2, y2, z2 = map(int, re.findall(r"\d+", line))
        assert x1 <= x2 and y1 <= y2 and z1 <= z2
        yield Brick(i, x1, y1, z1, x2, y2, z2)


@cache
def make_bricks_fall() -> list[Brick]:
    all_bricks = list(parse_bricks())
    bricks = deque(sorted(all_bricks, key=lambda b: b.z1))
    grid = {}

    for brick in bricks:
        for x, y, z in brick.get_volume():
            grid[(x, y, z)] = brick

    while bricks:
        brick = bricks.popleft()
        stucked, blocked = False, False
        z = brick.z1 - 1
        if z == 0:
            stucked = True
        else:
            for x, y in brick.get_surface():
                blocking_brick = grid.get((x, y, z))
                if blocking_brick and blocking_brick.floating:
                    blocked = True
                elif blocking_brick:
                    stucked = True
                    brick.supported_by.add(blocking_brick)
                    blocking_brick.supporting.add(brick)

        if stucked:
            brick.floating = False
        elif blocked:
            bricks.append(brick)
        else:
            brick.move_down()
            for x, y in brick.get_surface():
                del grid[(x, y, brick.z2 + 1)]
                grid[(x, y, brick.z1)] = brick
            bricks.appendleft(brick)
    return all_bricks


def count_safe(bricks: list[Brick]) -> int:
    count = 0
    for brick in bricks:
        for child in brick.supporting:
            if len(child.supported_by) == 1:
                break
        else:
            count += 1
    return count


def main1() -> int:
    bricks = make_bricks_fall()
    return count_safe(bricks)


def count_cascade(bricks: list[Brick]) -> int:
    def inner(brick: Brick, fallen: set[Brick]) -> set[Brick]:
        fallen.add(brick)
        for supported_brick in brick.supporting:
            if all(
                supporting_brick in fallen
                for supporting_brick in supported_brick.supported_by
            ):
                fallen |= inner(supported_brick, fallen)
        return fallen

    return sum(len(inner(brick, set())) - 1 for brick in bricks)


def main2() -> int:
    bricks = make_bricks_fall()
    return count_cascade(bricks)
