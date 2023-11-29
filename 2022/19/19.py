import re
from collections import defaultdict, deque
from dataclasses import dataclass
from enum import Enum
from functools import cached_property

from utils.parsing import parse_input


class Resource(Enum):
    ORE = 0
    CLAY = 1
    OBSIDIAN = 2
    GEODE = 3


@dataclass
class Blueprint:
    id: int
    costs: dict[Resource, list[tuple[Resource, int]]]

    @cached_property
    def max_robots_per_type(self) -> dict[Resource, int]:
        max_robots: dict[Resource, int] = {resource: 0 for resource in Resource}
        for costs in self.costs.values():
            for resource_type, count in costs:
                max_robots[resource_type] = max(max_robots[resource_type], count)
        max_robots[Resource.GEODE] = -1
        return max_robots

    def __hash__(self) -> int:
        return hash(self.id)


def parse_blueprints() -> list[Blueprint]:
    regex = re.compile(
        r"Blueprint (\d+): "
        r"Each ore robot costs (\d+) ore. "
        r"Each clay robot costs (\d+) ore. "
        r"Each obsidian robot costs (\d+) ore and (\d+) clay. "
        r"Each geode robot costs (\d+) ore and (\d+) obsidian."
    )
    blueprints: list[Blueprint] = []
    for line in parse_input():
        match = regex.match(line)
        if match is None:
            break

        groups = match.groups()
        costs = {
            Resource.ORE: [(Resource.ORE, int(groups[1]))],
            Resource.CLAY: [(Resource.ORE, int(groups[2]))],
            Resource.OBSIDIAN: [
                (Resource.ORE, int(groups[3])),
                (Resource.CLAY, int(groups[4])),
            ],
            Resource.GEODE: [
                (Resource.ORE, int(groups[5])),
                (Resource.OBSIDIAN, int(groups[6])),
            ],
        }
        blueprints.append(Blueprint(id=int(groups[0]), costs=costs))
    return blueprints


@dataclass
class State:
    blueprint: Blueprint
    robots: dict[Resource, int]
    resources: dict[Resource, int]
    countdown: int

    @property
    def score(self) -> int:
        return self.resources[Resource.GEODE]

    def _can_build_robot(self, robot_type: Resource) -> bool:
        cost = self.blueprint.costs[robot_type]
        for resource, count in cost:
            if self.resources[resource] < count:
                return False
        return True

    def _should_build_robot(self, robot_type: Resource) -> bool:
        if robot_type == Resource.GEODE:
            return True

        blueprint_limits = self.blueprint.max_robots_per_type
        if self.robots[robot_type] >= blueprint_limits[robot_type]:
            return False

        if (
            self.robots[robot_type] * self.countdown + self.resources[robot_type]
            >= blueprint_limits[robot_type] * self.countdown
        ):
            return False

        return True

    def build_robot(self, robot_type: Resource) -> None:
        cost = self.blueprint.costs[robot_type]
        for resource, count in cost:
            if self.resources[resource] < count:
                raise ValueError("Cannot build this robot")
            self.resources[resource] -= count
        self.robots[robot_type] += 1

    def get_resources(self) -> None:
        for robot_type, count in self.robots.items():
            self.resources[robot_type] += count

    def get_next_possible_builds(self) -> set[Resource | None]:
        if self.countdown == 0:
            return set()

        if self._can_build_robot(Resource.GEODE):
            # If we can build a geode robot, do it right away
            return {Resource.GEODE}

        if self.countdown == 1:
            # No need to build anything, we won't have enough time to build a new geode robot anyway
            return {None}

        states_to_try: set[Resource | None] = {None}
        for resource in {Resource.ORE, Resource.CLAY, Resource.OBSIDIAN}:
            if self._should_build_robot(resource) and self._can_build_robot(resource):
                states_to_try.add(resource)
        return states_to_try

    def build_next_state(self, build_type: Resource | None) -> "State":
        next_state = State(
            countdown=self.countdown - 1,
            blueprint=self.blueprint,
            resources={**self.resources},
            robots={**self.robots},
        )
        next_state.get_resources()
        if build_type is not None:
            next_state.build_robot(build_type)
        return next_state


class Factory:
    def __init__(self, blueprint: Blueprint, countdown: int) -> None:
        self.blueprint = blueprint
        self.countdown = countdown

    def run(self) -> int:
        start_node = State(
            blueprint=self.blueprint,
            robots={
                Resource.ORE: 1,
                Resource.CLAY: 0,
                Resource.OBSIDIAN: 0,
                Resource.GEODE: 0,
            },
            resources={
                Resource.ORE: 0,
                Resource.CLAY: 0,
                Resource.OBSIDIAN: 0,
                Resource.GEODE: 0,
            },
            countdown=self.countdown,
        )

        queue: deque[tuple[State, set[Resource | None]]] = deque([(start_node, set())])
        best_score_by_tick: dict[int, int] = defaultdict(int)
        while queue:
            state, previously_skipped_build_types = queue.popleft()
            if best_score_by_tick[state.countdown] > state.score:
                continue

            best_score_by_tick[state.countdown] = state.score
            next_possible_states = state.get_next_possible_builds()
            for build_type in next_possible_states:
                next_state = state.build_next_state(build_type)
                if build_type is None:
                    queue.append((next_state, next_possible_states))
                elif build_type in previously_skipped_build_types:
                    continue
                else:
                    queue.appendleft((next_state, set()))

        return best_score_by_tick[0]


def main1() -> int:
    blueprints = parse_blueprints()
    countdown = 24
    total = 0
    for blueprint in blueprints:
        factory = Factory(blueprint, countdown)
        score = factory.run()
        total += blueprint.id * score
    return total


def main2() -> int:
    blueprints = parse_blueprints()[:3]
    countdown = 32
    total = 1
    for blueprint in blueprints:
        factory = Factory(blueprint, countdown)
        score = factory.run()
        total *= score
    return total
