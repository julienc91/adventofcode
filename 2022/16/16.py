import re
from collections.abc import Iterable
from dataclasses import dataclass, field
from functools import cache


@dataclass
class Valve:
    name: str
    flow_rate: int
    links: set["Valve"] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Valve):
            return False
        return self.name == other.name


def parse_input() -> dict[str, Valve]:
    regex = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? (?P<links>(\w+(, )?)+)"
    )
    valves_by_name: dict[str, Valve] = {}
    try:
        while line := input().strip():
            match = regex.match(line)
            if not match:
                break

            groups = match.groups()
            name = groups[0]
            flow_rate = int(groups[1])
            links = match.group("links").split(", ")
            valve = Valve(name=name, flow_rate=flow_rate)
            for linked_valve_name in links:
                linked_valve = valves_by_name.get(linked_valve_name)
                if linked_valve:
                    valve.links.add(linked_valve)
                    linked_valve.links.add(valve)
            valves_by_name[valve.name] = valve
    except EOFError:
        pass
    return valves_by_name


@cache
def get_distance(start_valve: Valve, target_valve: Valve) -> int:
    queue = [(0, start_valve)]
    visited: set[Valve] = set()
    while queue:
        cost, valve = queue.pop(0)
        if valve in visited:
            continue

        visited.add(valve)
        if valve == target_valve:
            return cost

        for linked_valve in valve.links:
            if linked_valve not in visited:
                queue.append((cost + 1, linked_valve))
    return -1


def iterate_solo_paths(
    current_valve: Valve,
    visited: set[Valve],
    remaining_valves: set[Valve],
    remaining_minutes: int,
    current_score: int,
    current_score_per_minute: int,
) -> Iterable[tuple[set[Valve], int]]:
    if remaining_minutes <= 0:
        yield visited, current_score
        return

    # Discard valves that are too far to be of any help within the remaining time
    actual_remaining_valves = set()
    for valve in remaining_valves:
        distance = get_distance(current_valve, valve)
        if distance + 1 < remaining_minutes:
            actual_remaining_valves.add(valve)

    # Try each remaining valve, and attempt recursively to get the best score from there
    for valve in actual_remaining_valves:
        distance = get_distance(current_valve, valve)
        step_time = distance + 1
        new_remaining_minutes = remaining_minutes - step_time
        new_current_score = current_score + step_time * current_score_per_minute
        new_score_per_minute = current_score_per_minute + valve.flow_rate
        new_remaining_valves = set(actual_remaining_valves) - {valve}
        new_visited = set(visited) | {valve}
        yield from iterate_solo_paths(
            valve,
            new_visited,
            new_remaining_valves,
            new_remaining_minutes,
            new_current_score,
            new_score_per_minute,
        )

    yield visited, current_score + remaining_minutes * current_score_per_minute


def main1() -> int:
    valves_by_name = parse_input()
    total_time = 30

    start_valve = valves_by_name["AA"]
    assert start_valve.flow_rate == 0
    worthy_valves = {valve for valve in valves_by_name.values() if valve.flow_rate > 0}

    return max(
        score
        for _, score in iterate_solo_paths(
            start_valve, set(), worthy_valves, total_time, 0, 0
        )
    )


def main2() -> int:
    valves_by_name = parse_input()
    total_time = 26

    start_valve = valves_by_name["AA"]
    assert start_valve.flow_rate == 0
    worthy_valves = {valve for valve in valves_by_name.values() if valve.flow_rate > 0}

    best_score = 0
    all_paths = list(
        iterate_solo_paths(start_valve, set(), worthy_valves, total_time, 0, 0)
    )
    all_paths.sort(key=lambda item: item[1], reverse=True)

    # Hypothesis: the best solution uses two paths that are among the bests, we consider the top 10%
    all_paths = all_paths[: len(all_paths) // 10]

    for i in range(len(all_paths)):
        path1, score1 = all_paths[i]
        for j in range(i + 1, len(all_paths)):
            path2, score2 = all_paths[j]
            if not path1.isdisjoint(path2):
                # The paths are overlapping, this cannot be a valid solution
                continue
            if score1 + score2 > best_score:
                best_score = score1 + score2
    return best_score
