from collections.abc import Callable

from utils.enums import Direction
from utils.parsing import parse_input


def shoelace_formula(vertices: list[tuple[int, int]]):
    area = 0
    for i in range(len(vertices) - 1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        area += x1 * y2 - x2 * y1
    return abs(area) // 2


def _main(parse_line: Callable[[str], tuple[Direction, int]]) -> int:
    x, y = 0, 0
    total_edges = 1
    vertices = []
    for line in parse_input():
        direction, count = parse_line(line)
        x, y = direction.move(x, y, steps=count)
        vertices.append((x, y))
        total_edges += count
    return shoelace_formula(vertices) + (total_edges + 1) // 2


def main1() -> int:
    direction_mapping = {
        "U": Direction.TOP,
        "L": Direction.LEFT,
        "R": Direction.RIGHT,
        "D": Direction.BOTTOM,
    }

    def parse_line(line: str) -> tuple[Direction, int]:
        direction, count, _ = line.split()
        return direction_mapping[direction], int(count)

    return _main(parse_line)


def main2() -> int:
    direction_mapping = {
        "0": Direction.RIGHT,
        "1": Direction.BOTTOM,
        "2": Direction.LEFT,
        "3": Direction.TOP,
    }

    def parse_line(line: str) -> tuple[Direction, int]:
        _, _, color_code = line.split()
        count = int(color_code[2:7], 16)
        direction = direction_mapping[color_code[-2]]
        return direction, count

    return _main(parse_line)
