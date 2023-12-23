import itertools
from collections import deque
from dataclasses import dataclass, field

from utils.enums import Direction
from utils.parsing import parse_input


@dataclass
class Node:
    position: tuple[int, int]
    is_start: bool = False
    is_end: bool = False

    neighbours: set[tuple["Node", int]] = field(default_factory=set)

    def __hash__(self) -> int:
        return hash(self.position)

    def __repr__(self) -> str:
        return f"Node(position={self.position})"


def get_neighbours(
    x: int, y: int, maze: list[str], directed: bool
) -> list[tuple[int, int]]:
    neighbours = []
    current_value = maze[y][x]
    if directed and current_value in "<>v^":
        index = "<>v^".index(current_value)
        directions = [
            [Direction.LEFT, Direction.RIGHT, Direction.BOTTOM, Direction.TOP][index]
        ]
    else:
        directions = list(Direction)

    for direction in directions:
        x2, y2 = direction.move(x, y)
        if x2 < 0 or y2 < 0:
            continue

        try:
            value = maze[y2][x2]
        except IndexError:
            continue

        if value == "#":
            continue

        neighbours.append((x2, y2))
    return neighbours


def maze_to_graph(maze: list[str], directed: bool) -> list[Node]:
    start = (next(x for x in range(len(maze[0])) if maze[0][x] == "."), 0)
    end = (next(x for x in range(len(maze[-1])) if maze[-1][x] == "."), len(maze) - 1)

    nodes_by_position = {
        start: Node(start, is_start=True),
        end: Node(end, is_end=True),
    }

    for x, y in itertools.product(range(len(maze[0])), range(len(maze))):
        value = maze[y][x]
        if value == "#":
            continue

        neighbours = get_neighbours(x, y, maze, directed=False)
        assert 1 <= len(neighbours) <= 4, (neighbours, x, y)
        if len(neighbours) <= 2:
            continue

        nodes_by_position[(x, y)] = Node((x, y))

    queue: deque[tuple[tuple[int, int], Node, int]] = deque(
        [(Direction.BOTTOM.move(start[0], start[1]), nodes_by_position[start], 0)]
    )
    visited: set[tuple[tuple[int, int], Node]] = {(start, nodes_by_position[start])}
    while queue:
        position, previous_node, length = queue.popleft()
        if (position, previous_node) in visited:
            continue

        length += 1
        (x, y) = position
        visited.add((position, previous_node))
        if position in nodes_by_position:
            node = nodes_by_position[position]
            previous_node.neighbours.add((node, length))
            previous_node = node
            length = 0

        for next_position in get_neighbours(x, y, maze, directed=directed):
            queue.appendleft((next_position, previous_node, length))

    return list(nodes_by_position.values())


def _main(directed: bool) -> int:
    maze = list(parse_input())
    nodes = maze_to_graph(maze, directed=directed)
    start_node = next(node for node in nodes if node.is_start)

    def inner(node: Node, visited: set[Node]):
        if node.is_end:
            return 0

        res = -1
        visited.add(node)
        for next_node, length in node.neighbours:
            if next_node in visited:
                continue

            subtotal = inner(next_node, visited)
            if subtotal >= 0:
                res = max(res, length + subtotal)

        visited.remove(node)
        return res

    return inner(start_node, set())


def main1() -> int:
    return _main(directed=True)


def main2() -> int:
    return _main(directed=False)
