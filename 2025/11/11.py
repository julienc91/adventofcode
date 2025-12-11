from collections import defaultdict
from functools import cache

from utils.parsing import parse_input


def parse_graph() -> dict[str, set[str]]:
    graph = defaultdict(set)
    for line in parse_input():
        left, *right = line.split(" ")
        left = left[:-1]
        graph[left] = set(right)
    return graph


def count_paths(graph: dict[str, set[str]], start: str, end: str) -> int:
    @cache
    def inner(current: str) -> int:
        if current == end:
            return 1
        return sum(inner(child) for child in graph[current])

    return inner(start)


def main1() -> int:
    graph = parse_graph()
    return count_paths(graph, "you", "out")


def main2() -> int:
    graph = parse_graph()
    return (
        count_paths(graph, "svr", "fft")
        * count_paths(graph, "fft", "dac")
        * count_paths(graph, "dac", "out")
    ) + (
        count_paths(graph, "svr", "dac")
        * count_paths(graph, "dac", "fft")
        * count_paths(graph, "fft", "out")
    )
