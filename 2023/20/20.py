import math

from utils.parsing import parse_input


class Node:
    def __init__(self, name: str):
        self.name = name
        self.parents: list[str] = []
        self.children: list[str] = []

        self.low_count: int = 0
        self.high_count: int = 0

    def execute(self, received: tuple[str, int] | None) -> dict[str, int]:
        return {}

    def _send(self, signal: int) -> dict[str, int]:
        if signal == 1:
            self.high_count += len(self.children)
        else:
            self.low_count += len(self.children)
        return {child_name: signal for child_name in self.children}


class Button(Node):
    def __init__(self):
        super().__init__("button")
        self.children = ["broadcaster"]

    def execute(self, received: None) -> dict[str, int]:
        assert received is None
        return self._send(0)


class Broadcaster(Node):
    def __init__(self):
        super().__init__("broadcaster")
        self.parents = ["button"]

    def execute(self, received: tuple[str, int]) -> dict[str, int]:
        _, signal_ = received
        return self._send(signal_)


class FlipFlop(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.state = False

    def execute(self, received: tuple[str, int]) -> dict[str, int]:
        _, signal = received
        if signal == 1:
            return {}

        self.state = not self.state
        signal = 1 if self.state else 0
        return self._send(signal)


class Conjunction(Node):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.memory = {}

    def execute(self, received: tuple[str, int]) -> dict[str, int]:
        received_from, signal = received
        self.memory[received_from] = signal
        signal = (
            0
            if all(self.memory.get(parent_name, 0) == 1 for parent_name in self.parents)
            else 1
        )
        return self._send(signal)


class Program:
    def __init__(
        self, nodes: dict[str, Node], monitor_conjunction: str | None = None
    ) -> None:
        self.nodes = nodes
        self.iterations = 1
        self.monitor_conjunction = monitor_conjunction
        self.cycles = {}

    def execute(self) -> None:
        queue: list[tuple[str, tuple[str, int] | None]] = [("button", None)]
        while queue:
            node_name, params = queue.pop(0)
            node = self.nodes[node_name]
            signals = node.execute(params)
            for child_name, signal in signals.items():
                if child_name == self.monitor_conjunction and signal == 1:
                    if node_name in self.cycles:
                        assert self.iterations % self.cycles[node_name] == 0
                    else:
                        self.cycles[node_name] = self.iterations
                queue.append((child_name, (node_name, signal)))

        self.iterations += 1


def get_node_from_node_name(full_name: str) -> Node:
    if full_name == "broadcaster":
        return Broadcaster()
    elif full_name.startswith("%"):
        return FlipFlop(full_name[1:])
    elif full_name.startswith("&"):
        return Conjunction(full_name[1:])
    raise ValueError(f"Unexpected node name: {full_name}")


def parse_nodes() -> dict[str, Node]:
    nodes_by_name = {}
    for line in parse_input():
        parent, children = line.split(" -> ")
        node = get_node_from_node_name(parent)
        nodes_by_name[node.name] = node
        for child_name in children.split(", "):
            node.children.append(child_name)

    missing_nodes = []
    for node in nodes_by_name.values():
        for child_name in node.children:
            if child_name not in nodes_by_name:
                missing_node = Node(child_name)
                missing_node.parents.append(node.name)
                missing_nodes.append(missing_node)
            else:
                child = nodes_by_name[child_name]
                child.parents.append(node.name)

    for node in missing_nodes:
        nodes_by_name[node.name] = node

    nodes_by_name["button"] = Button()
    return nodes_by_name


def main1() -> int:
    nodes = parse_nodes()
    program = Program(nodes)
    while program.iterations <= 1000:
        program.execute()

    total_low = sum(node.low_count for node in nodes.values())
    total_high = sum(node.high_count for node in nodes.values())
    return total_low * total_high


def main2() -> int:
    nodes = parse_nodes()

    parent_names = nodes["rx"].parents
    assert len(parent_names) == 1
    parent_name = next(iter(parent_names))
    parent = nodes[parent_name]
    assert isinstance(parent, Conjunction)

    nodes_to_track = parent.parents
    program = Program(nodes, monitor_conjunction=parent_name)
    while len(program.cycles) < len(nodes_to_track):
        program.execute()

    return math.lcm(*program.cycles.values())
