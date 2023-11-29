import itertools
import re
from collections import deque
from collections.abc import Iterator
from dataclasses import dataclass

from utils.parsing import parse_input


@dataclass
class Generator:
    name: str

    def is_microship_available(self, floor: "Floor") -> bool:
        return any(microship.name == self.name for microship in floor.microships)


@dataclass
class Microship:
    name: str


@dataclass
class Floor:
    number: int
    generators: tuple[Generator, ...] = ()
    microships: tuple[Microship, ...] = ()


@dataclass
class Map:
    floors: tuple[Floor, ...] = ()
    elevator: int = 0
    steps: int = 0

    @property
    def is_over(self) -> bool:
        return all(
            len(floor.generators) == len(floor.microships) == 0
            for floor in self.floors[:-1]
        )

    @property
    def state_id(self) -> str:
        return f"{self.elevator}" + "".join(
            f"{floor.number}:{len(floor.generators)}:{len(floor.microships)}"
            for floor in self.floors
        )

    def list_possibilities(
        self,
    ) -> Iterator[tuple[tuple[Generator | Microship, ...], int]]:
        target_floors: list[int] = []
        if self.elevator > 0:
            target_floors.append(self.elevator - 1)
        if self.elevator < len(self.floors) - 1:
            target_floors.append(self.elevator + 1)

        floor = self.floors[self.elevator]

        for i in range(2):
            for t in itertools.combinations(floor.generators + floor.microships, i + 1):
                for target_floor in target_floors:
                    if self.is_move_valid(t, target_floor):
                        yield t, target_floor

    @staticmethod
    def validate_combination(
        generators: tuple[Generator, ...], microships: tuple[Microship, ...]
    ) -> bool:
        for microship in microships:
            if (
                all(g.name != microship.name for g in generators)
                and len(generators) > 0
            ):
                return False
        return True

    def is_move_valid(
        self, move: tuple[Generator | Microship, ...], target_floor: int
    ) -> bool:
        if not move:
            return False

        new_generators_current_floor = tuple(
            g for g in self.floors[self.elevator].generators if g not in move
        )
        new_microships_current_floor = tuple(
            m for m in self.floors[self.elevator].microships if m not in move
        )
        if not self.validate_combination(
            new_generators_current_floor, new_microships_current_floor
        ):
            return False

        new_generators_new_floor = (
            tuple(g for g in move if isinstance(g, Generator))
            + self.floors[target_floor].generators
        )
        new_microships_new_floor = (
            tuple(m for m in move if isinstance(m, Microship))
            + self.floors[target_floor].microships
        )
        if not self.validate_combination(
            new_generators_new_floor, new_microships_new_floor
        ):
            return False
        return True

    def make_move(
        self, move: tuple[Generator | Microship, ...], target_floor: int
    ) -> "Map":
        new_map = Map()
        for floor in self.floors:
            new_floor = Floor(floor.number)
            if floor.number == self.elevator:
                new_floor.generators = tuple(
                    g for g in floor.generators if g not in move
                )
                new_floor.microships = tuple(
                    m for m in floor.microships if m not in move
                )
            elif floor.number == target_floor:
                new_floor.generators = (
                    tuple(g for g in move if isinstance(g, Generator))
                    + floor.generators
                )
                new_floor.microships = (
                    tuple(m for m in move if isinstance(m, Microship))
                    + floor.microships
                )
            else:
                new_floor.generators = floor.generators
                new_floor.microships = floor.microships
            new_map.floors += (new_floor,)
            new_map.elevator = target_floor
        new_map.steps = self.steps + 1
        return new_map


def parse_map() -> Map:
    m = Map()
    for line in parse_input():
        floor = Floor(number=len(m.floors))
        for match in re.findall(r"\w+ generator", line):
            name = match.split()[0]
            floor.generators += (Generator(name=name),)
        for match in re.findall(r"\w+-compatible microchip", line):
            name = match.split("-")[0]
            floor.microships += (Microship(name=name),)
        m.floors += (floor,)
    return m


def _main(start_map: Map) -> int:
    stack: deque[Map] = deque([start_map])
    visited: set[str] = set()

    while m := stack.popleft():
        if m.is_over:
            return m.steps

        for move, target_floor in m.list_possibilities():
            new_map = m.make_move(move, target_floor)
            if (state_id := new_map.state_id) not in visited:
                visited.add(state_id)
                stack.append(new_map)
    raise RuntimeError("No solution found")


def main1() -> int:
    start_map = parse_map()
    return _main(start_map)


def main2() -> int:
    start_map = parse_map()
    start_map.floors[0].generators += (
        Generator(name="elerium"),
        Generator(name="dilithium"),
    )
    start_map.floors[0].microships += (
        Microship(name="elerium"),
        Microship(name="dilithium"),
    )
    return _main(start_map)
