import itertools
from collections import deque
from dataclasses import dataclass, field

from utils.enums import Direction
from utils.parsing import parse_input


@dataclass
class Node:
    id: int
    is_start: bool = False
    is_end: bool = False

    neighbours: list[tuple[int, int]] = field(default_factory=list)


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

    node_counter = itertools.count()
    nodes_by_position = {
        start: Node(id=next(node_counter), is_start=True),
        end: Node(id=next(node_counter), is_end=True),
    }

    for x, y in itertools.product(range(len(maze[0])), range(len(maze))):
        value = maze[y][x]
        if value == "#":
            continue

        neighbours = get_neighbours(x, y, maze, directed=False)
        if len(neighbours) > 2:
            nodes_by_position[(x, y)] = Node(id=next(node_counter))

    queue: deque[tuple[tuple[int, int], Node, int]] = deque(
        [((start[0], start[1] + 1), nodes_by_position[start], 0)]
    )
    visited: set[tuple[tuple[int, int], int]] = {(start, nodes_by_position[start].id)}
    while queue:
        position, previous_node, length = queue.popleft()
        if (position, previous_node.id) in visited:
            continue

        length += 1
        (x, y) = position
        visited.add((position, previous_node.id))
        if position in nodes_by_position:
            node = nodes_by_position[position]
            previous_node.neighbours.append((node.id, length))
            previous_node = node
            length = 0

        for next_position in get_neighbours(x, y, maze, directed=directed):
            queue.appendleft((next_position, previous_node, length))

    return sorted(nodes_by_position.values(), key=lambda n: n.id)


def _main(directed: bool) -> int:
    maze = list(parse_input())
    nodes = maze_to_graph(maze, directed=directed)
    start_node = next(node for node in nodes if node.is_start)
    visited: list[bool] = [False for _ in nodes]

    def inner(node_id: int):
        node = nodes[node_id]
        if node.is_end:
            return 0

        res = -1
        visited[node.id] = True
        for next_node_id, length in node.neighbours:
            if visited[next_node_id]:
                continue

            subtotal = inner(next_node_id)
            if subtotal >= 0 and subtotal >= res - length:
                res = length + subtotal

        visited[node.id] = False
        return res

    return inner(start_node.id)


def main1() -> int:
    return _main(directed=True)


def main2() -> int:
    return _main(directed=False)
