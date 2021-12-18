import heapq
from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int
    weight: int
    links: set["Node"]

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __repr__(self) -> str:
        return f"({self.x}, {self.y}): {self.weight}"

    def __lt__(self, other: "Node") -> bool:
        return self.x < other.x or (self.x == other.x and self.y < other.y)


def create_links_between_nodes(
    nodes_by_coordinates: dict[tuple[int, int], Node]
) -> None:
    for (x, y), node in nodes_by_coordinates.items():
        neighbours = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        for x2, y2 in neighbours:
            neighbour = nodes_by_coordinates.get((x2, y2))
            if neighbour:
                node.links.add(neighbour)


def make_tiling(
    base_grid_size: int, nodes_by_coordinates: dict[tuple[int, int], Node], tiling: int
) -> None:
    if tiling <= 1:
        return

    for x in range(base_grid_size):
        for y in range(base_grid_size):
            node = nodes_by_coordinates[(x, y)]

            for i in range(tiling):
                for j in range(tiling):
                    if i == 0 and j == 0:
                        continue

                    new_x = base_grid_size * i + x
                    new_y = base_grid_size * j + y
                    new_weight = node.weight + i + j
                    if new_weight > 9:
                        new_weight = (new_weight % 10) + 1

                    new_node = Node(x=new_x, y=new_y, weight=new_weight, links=set())
                    nodes_by_coordinates[(new_x, new_y)] = new_node


def parse_graph(tiling: int) -> tuple[Node, Node]:
    nodes_by_coordinates = {}
    y = 0
    try:
        while line := input().strip():
            for x, w in enumerate(line):
                nodes_by_coordinates[(x, y)] = Node(
                    x=x, y=y, weight=int(w), links=set()
                )
            y += 1
    except EOFError:
        pass

    base_grid_size = y
    make_tiling(base_grid_size, nodes_by_coordinates, tiling)
    grid_size = y * tiling - 1

    create_links_between_nodes(nodes_by_coordinates)
    return nodes_by_coordinates[(0, 0)], nodes_by_coordinates[(grid_size, grid_size)]


def shortest_path(root_node: Node, target_node: Node) -> int:
    queue = [(0, root_node)]
    visited = set()
    while queue:
        cost, node = heapq.heappop(queue)
        if node in visited:
            continue

        visited.add(node)
        if node == target_node:
            return cost

        for neighbour in node.links:
            if neighbour not in visited:
                heapq.heappush(queue, (cost + neighbour.weight, neighbour))
    return -1


def main1() -> int:
    root_node, target_node = parse_graph(tiling=1)
    return shortest_path(root_node, target_node)


def main2() -> int:
    root_node, target_node = parse_graph(tiling=5)
    return shortest_path(root_node, target_node)
