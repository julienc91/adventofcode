from collections.abc import Iterator


class Node:
    def __init__(self):
        self.parent: "Node | None" = None
        self.children: list["Node"] = []
        self.metadata: list[int] = []

    @property
    def sum_metadata(self):
        return sum(self.metadata)

    @property
    def value(self):
        if not self.children:
            return self.sum_metadata

        return sum(
            self.children[i - 1].value
            for i in self.metadata
            if 0 < i <= len(self.children)
        )


def get_root_node() -> Node:
    numbers = map(int, input().split())
    return read_node(numbers)


def read_node(stream: Iterator[int]) -> Node:
    nb_children = next(stream)
    nb_metadata = next(stream)
    node = Node()

    for _ in range(nb_children):
        child = read_node(stream)
        child.parent = node
        node.children.append(child)

    node.metadata = [next(stream) for _ in range(nb_metadata)]
    return node


def iter_nodes(root: Node) -> Iterator[Node]:
    yield root
    for child in root.children:
        yield from iter_nodes(child)


def main1() -> int:
    root = get_root_node()
    return sum(node.sum_metadata for node in iter_nodes(root))


def main2() -> int:
    return get_root_node().value
