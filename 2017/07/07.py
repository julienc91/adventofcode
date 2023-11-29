from collections import defaultdict

from utils.parsing import parse_input


class Node:
    def __init__(self, name: str) -> None:
        self.name = name
        self.weight: int = 0
        self.parent: "Node | None" = None
        self.children: list["Node"] = []

    def add_child(self, node: "Node") -> None:
        self.children.append(node)
        node.parent = self

    @property
    def total_weight(self) -> int:
        return self.weight + sum(child.total_weight for child in self.children)


class Tree:
    def __init__(self) -> None:
        self.nodes_by_name: dict[str, Node] = {}

    def add_node(self, name: str, weight: int, children: list[str]) -> None:
        node = self.get_node(name)
        node.weight = weight
        for child_name in children:
            node.add_child(self.get_node(child_name))

    def get_node(self, name: str) -> Node:
        if name not in self.nodes_by_name:
            self.nodes_by_name[name] = Node(name)
        return self.nodes_by_name[name]

    @property
    def root(self) -> Node:
        return next(node for node in self.nodes_by_name.values() if node.parent is None)


def get_tree() -> Tree:
    tree = Tree()
    for line in parse_input():
        left, _, right = line.partition(" -> ")
        name, weight = left.split()
        children = right.split(", ") if right else []
        tree.add_node(name, int(weight[1:-1]), children)
    return tree


def main1() -> str:
    return get_tree().root.name


def main2() -> int:
    tree = get_tree()
    queue = [tree.root]
    node_to_fix = queue[0]
    while queue:
        root = queue.pop(0)
        weights = [child.total_weight for child in root.children]
        if len(set(weights)) <= 1:
            continue
        else:
            queue += [child for child in root.children]
            node_to_fix = root

    children_by_total_weight: dict[int, list[Node]] = defaultdict(list)
    for child in node_to_fix.children:
        children_by_total_weight[child.total_weight].append(child)

    assert len(children_by_total_weight) == 2
    node_to_fix = next(
        nodes[0] for nodes in children_by_total_weight.values() if len(nodes) <= 1
    )
    total_weight_to_target = next(
        nodes[0].total_weight
        for nodes in children_by_total_weight.values()
        if len(nodes) > 1
    )

    return total_weight_to_target - (node_to_fix.total_weight - node_to_fix.weight)
