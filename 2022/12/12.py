from dataclasses import dataclass, field


@dataclass
class Node:
    id: tuple[int, int]
    level: int
    links: list["Node"] = field(default_factory=list)


def parse_input() -> tuple[
    dict[tuple[int, int], Node], tuple[int, int], tuple[int, int]
]:
    nodes_by_id: dict[tuple[int, int], Node] = {}
    start = (0, 0)
    finish = (0, 0)
    y = 0

    try:
        while line := input().strip():
            for x, level in enumerate(line):
                if level == "S":
                    level = "a"
                    start = (x, y)
                elif level == "E":
                    level = "z"
                    finish = (x, y)

                node = Node(id=(x, y), level=ord(level))
                nodes_by_id[(x, y)] = node
            y += 1
    except EOFError:
        pass

    for node in nodes_by_id.values():
        x, y = node.id
        for x2, y2 in [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]:
            neighbour = nodes_by_id.get((x2, y2))
            if neighbour is None:
                continue

            if neighbour.level <= node.level + 1:
                node.links.append(neighbour)

    return nodes_by_id, start, finish


def shortest_path(root_node: Node, target_node: Node) -> int:
    queue = [(0, root_node)]
    visited = set()
    while queue:
        cost, node = queue.pop(0)
        if node.id in visited:
            continue

        visited.add(node.id)
        if node == target_node:
            return cost

        for neighbour in node.links:
            if neighbour.id not in visited:
                queue.append((cost + 1, neighbour))
    return -1


def main1() -> int:
    nodes, start, finish = parse_input()
    return shortest_path(nodes[start], nodes[finish])


def main2() -> int:
    nodes, _, finish = parse_input()
    shortest_path_length = len(nodes)
    for node in nodes.values():
        if node.level != ord("a"):
            continue

        path_length = shortest_path(node, nodes[finish])
        if path_length > 0:
            shortest_path_length = min(shortest_path_length, path_length)
    return shortest_path_length
