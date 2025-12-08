import itertools
import math
from collections.abc import Iterator

from utils.parsing import parse_input

Point = tuple[int, int, int]


def parse_positions() -> list[Point]:
    res = []
    for line in parse_input():
        x, y, z = map(int, line.split(","))
        res.append((x, y, z))
    return res


def cache_distances(positions: list[Point]) -> list[tuple[Point, Point]]:
    def distance(a: Point, b: Point) -> float:
        return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2

    res = list(itertools.combinations(positions, 2))
    res.sort(key=lambda o: distance(o[0], o[1]))
    return res


def _main(
    positions_by_circuit_id: dict[int, list[Point]] | None = None,
) -> Iterator[tuple[Point, Point]]:
    positions = parse_positions()
    distances = cache_distances(positions)

    if positions_by_circuit_id is None:
        positions_by_circuit_id = {}
    positions_by_circuit_id |= {i: [position] for i, position in enumerate(positions)}
    circuit_id_by_position = {position: i for i, position in enumerate(positions)}

    def merge_circuits(a: int, b: int) -> None:
        positions_by_circuit_id[a] += positions_by_circuit_id[b]
        for pos in positions_by_circuit_id[b]:
            circuit_id_by_position[pos] = a
        del positions_by_circuit_id[b]

    while len(positions_by_circuit_id) > 1:
        pos1, pos2 = distances.pop(0)
        yield pos1, pos2
        u, v = circuit_id_by_position[pos1], circuit_id_by_position[pos2]
        if u != v:
            merge_circuits(u, v)


def main1() -> int:
    positions_by_circuit_id = {}
    iterator = _main(positions_by_circuit_id)
    for _ in range(1000):
        next(iterator)

    circuits_lengths = sorted(
        [len(positions) for positions in positions_by_circuit_id.values()], reverse=True
    )
    return math.prod(circuits_lengths[:3])


def main2() -> int:
    iterator = _main()
    *_, (a, b) = iterator
    return a[0] * b[0]
