import itertools
from collections import defaultdict

from utils.parsing import parse_input


def parse_connections() -> dict[str, set[str]]:
    res = defaultdict(set)
    for line in parse_input():
        n1, n2 = line.split("-")
        res[n1].add(n2)
        res[n2].add(n1)
    return res


def main1() -> int:
    neighbours_by_nodes = parse_connections()
    all_nodes = neighbours_by_nodes.keys()
    groups = set()
    nodes_starting_with_t = {n for n in all_nodes if n.startswith("t")}
    for n1 in nodes_starting_with_t:
        for n2, n3 in itertools.combinations(neighbours_by_nodes[n1] - {n1}, 2):
            if _check_valid_group({n1, n2, n3}, neighbours_by_nodes):
                groups.add(frozenset((n1, n2, n3)))
    return len(groups)


def _check_valid_group(
    group: set[str], neighbours_by_nodes: dict[str, set[str]]
) -> bool:
    return all(
        n1 in neighbours_by_nodes[n2] for n1 in group for n2 in group if n1 != n2
    )


def main2() -> str:
    neighbours_by_nodes = parse_connections()
    max_group = set()
    for n1, neighbours in neighbours_by_nodes.items():
        for n2 in neighbours:
            group = (neighbours & neighbours_by_nodes[n2]) | {n1, n2}
            if len(group) > len(max_group) and _check_valid_group(
                group, neighbours_by_nodes
            ):
                max_group = group

    return ",".join(sorted(max_group))
