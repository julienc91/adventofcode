import re
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from utils.parsing import parse_input


@dataclass
class Node:
    name: str
    neighbours: list[tuple["Node", int]]

    def __repr__(self) -> str:
        return self.name


def build_graph() -> dict[str, Node]:
    graph = {}
    regex = re.compile(r"(\w+) to (\w+) = (\d+)")
    for line in parse_input():
        match = regex.search(line)
        assert match
        a, b, d = match.group(1), match.group(2), int(match.group(3))

        if a not in graph:
            graph[a] = Node(name=a, neighbours=[])
        if b not in graph:
            graph[b] = Node(name=b, neighbours=[])

        graph[a].neighbours.append((graph[b], d))
        graph[b].neighbours.append((graph[a], d))
    return graph


def find_path(graph: dict[str, Node], compare: Callable[[Iterable[int]], int]) -> int:
    def inner(stack: list[Node], current_distance: int) -> int:
        if len(stack) == len(graph):
            return current_distance

        last_node = stack[-1]
        not_visited_nodes = [
            (node, distance)
            for node, distance in last_node.neighbours
            if node not in stack
        ]
        if not not_visited_nodes and len(stack) < len(graph):
            return -1

        distances = []
        for node, distance in not_visited_nodes:
            new_stack = [*stack, node]
            new_distance = inner(new_stack, current_distance + distance)
            if new_distance > 0:
                distances.append(new_distance)

        if distances:
            return compare(distances)
        return -1

    return compare(inner([n], 0) for n in graph.values())


def main1() -> int:
    graph = build_graph()
    return find_path(graph, min)


def main2() -> int:
    graph = build_graph()
    return find_path(graph, max)
