import os.path
from dataclasses import dataclass
from functools import cached_property


@dataclass
class Node:
    name: str
    size: int
    used: int

    is_target: bool = False
    is_destination: bool = False

    @property
    def available(self) -> int:
        return self.size - self.used

    @cached_property
    def x(self) -> int:
        return int(self.name.split("-")[1][1:])

    @cached_property
    def y(self) -> int:
        return int(self.name.split("-")[2][1:])


def parse_nodes() -> list[Node]:
    input(), input()
    res: list[Node] = []
    try:
        while line := input().strip():
            path, size, used, _, _ = line.split()
            res.append(
                Node(
                    name=os.path.basename(path),
                    size=int(size[:-1]),
                    used=int(used[:-1]),
                )
            )
    except EOFError:
        pass
    return res


def is_viable(node_a: Node, node_b: Node) -> bool:
    return node_a is not node_b and 0 < node_a.used <= node_b.available


def main1() -> int:
    nodes = parse_nodes()
    count_viable_pairs = 0
    for node_a in nodes:
        for node_b in nodes:
            if node_a is node_b:
                continue
            if is_viable(node_a, node_b):
                count_viable_pairs += 1
    return count_viable_pairs


def main2() -> int:
    nodes = parse_nodes()
    highest_x = max(node.x for node in nodes)

    # G....................................T
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......################################
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ......................................
    # ................_.....................
    # ......................................
    # ......................................

    empty_node = next(node for node in nodes if node.used == 0)
    leftmost_full_node = sorted(
        [node for node in nodes if node.used > 400], key=lambda node: node.x
    )[0]

    count = (
        empty_node.x - leftmost_full_node.x + 1
    )  # Go left until we can go straight up
    count += empty_node.y  # Go straight up
    count += highest_x - leftmost_full_node.x + 1  # Go right until we reach the target
    count += (
        highest_x - 1
    ) * 5  # Loop around the target to move it to the leftmost node
    return count
