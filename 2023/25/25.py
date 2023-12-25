import heapq
import random
from collections import Counter, defaultdict

from utils.parsing import parse_input


def shortest_path(nodes, n1, n2):
    queue: list[tuple[int, str, list[frozenset[str]]]] = [(0, n1, [])]
    visited = set()

    while queue:
        length, node, path = heapq.heappop(queue)
        if node in visited:
            continue

        visited.add(node)
        if node == n2:
            return path

        for neighbour in nodes[node]:
            if neighbour not in visited:
                heapq.heappush(
                    queue,
                    (length + 1, neighbour, path + [frozenset([node, neighbour])]),
                )


def find_cut(nodes):
    """
    Assume that the cut will be on the 3 most frequently seen nodes on paths between two random nodes.
    This should be true if both "parts" of the graph are large enough.
    """
    node_names = list(nodes.keys())
    counter = Counter()
    for _ in range(500):
        n1 = random.choice(node_names)
        n2 = random.choice(node_names)
        if n1 == n2:
            continue

        path = shortest_path(nodes, n1, n2)
        counter.update(path)

    return [edge for edge, _ in counter.most_common(3)]


def main1() -> int:
    nodes = defaultdict(set)

    for line in parse_input():
        n1, *others = line.replace(":", "").split()
        for n2 in others:
            nodes[n1].add(n2)
            nodes[n2].add(n1)

    cut = find_cut(nodes)
    for u, v in cut:
        nodes[u].remove(v)
        nodes[v].remove(u)

    start_node = random.choice(list(nodes.keys()))
    queue = [start_node]
    group = set()
    while queue:
        node = queue.pop(0)
        if node in group:
            continue

        group.add(node)
        queue += list(nodes[node])

    return len(group) * (len(nodes) - len(group))


def main2() -> int:
    return -1
