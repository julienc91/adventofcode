import itertools
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass
from functools import cache, cached_property

from utils.parsing import parse_input


@dataclass
class Scanner:
    name: str
    beacons: list[tuple[int, int, int]]
    location: tuple[int, int, int] = (0, 0, 0)

    def __hash__(self) -> int:
        return hash(self.name)

    @cached_property
    def distances(self) -> list[float]:
        res = []
        for i, j in itertools.combinations(range(len(self.beacons)), 2):
            x1, y1, z1 = self.beacons[i]
            x2, y2, z2 = self.beacons[j]

            distance = round(
                ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5, 5
            )
            res.append(distance)
        return res


rotations = [
    lambda x, y, z: (x, y, z),
    lambda x, y, z: (x, -z, y),
    lambda x, y, z: (x, -y, -z),
    lambda x, y, z: (x, z, -y),
    lambda x, y, z: (-x, -y, z),
    lambda x, y, z: (-x, -z, -y),
    lambda x, y, z: (-x, y, -z),
    lambda x, y, z: (-x, z, y),
    lambda x, y, z: (-z, x, -y),
    lambda x, y, z: (y, x, -z),
    lambda x, y, z: (z, x, y),
    lambda x, y, z: (-y, x, z),
    lambda x, y, z: (z, -x, -y),
    lambda x, y, z: (y, -x, z),
    lambda x, y, z: (-z, -x, y),
    lambda x, y, z: (-y, -x, -z),
    lambda x, y, z: (-y, -z, x),
    lambda x, y, z: (z, -y, x),
    lambda x, y, z: (y, z, x),
    lambda x, y, z: (-z, y, x),
    lambda x, y, z: (z, y, -x),
    lambda x, y, z: (-y, z, -x),
    lambda x, y, z: (-z, -y, -x),
    lambda x, y, z: (y, -z, -x),
]


def parse_scanners() -> list[Scanner]:
    scanners: list[Scanner] = []
    scanner = None
    for line in parse_input():
        if line.startswith("---"):
            scanner = Scanner(name=str(len(scanners)), beacons=[])
            scanners.append(scanner)
        elif line:
            assert scanner
            x, y, z = map(int, line.split(","))
            scanner.beacons.append((x, y, z))
    return scanners


def get_neighbour_scanner(
    scanner: Scanner, located_scanners: list[Scanner]
) -> Scanner | None:
    min_common_distances = 66  # 11 + 10 + 9 + ... + 1
    for other_scanner in located_scanners:
        common_distances = 0
        for d1 in scanner.distances:
            if d1 in other_scanner.distances:
                common_distances += 1

        if common_distances >= min_common_distances:
            return other_scanner
    return None


def apply_rotation(
    scanner: Scanner, rotation: Callable[[int, int, int], tuple[int, int, int]]
) -> Scanner:
    return Scanner(
        name=scanner.name,
        beacons=[rotation(*coordinates) for coordinates in scanner.beacons],
        location=rotation(*scanner.location),
    )


def apply_translation(scanner: Scanner, vector: tuple[int, int, int]) -> Scanner:
    vx, vy, vz = vector
    sx, sy, sz = scanner.location
    return Scanner(
        name=scanner.name,
        beacons=[(x + vx, y + vy, z + vz) for x, y, z in scanner.beacons],
        location=(sx + vx, sy + vy, sz + vz),
    )


def count_similarities(scanner: Scanner, ref: Scanner) -> int:
    beacons_s1 = set(scanner.beacons)
    beacons_s2 = set(ref.beacons)
    return len(beacons_s1 & beacons_s2)


def find_rotation(scanner: Scanner, ref: Scanner) -> Scanner:
    for rotation in rotations:
        rotated_scanner = apply_rotation(scanner, rotation)
        for x2, y2, z2 in ref.beacons:
            for x1, y1, z1 in rotated_scanner.beacons:
                vector = (x2 - x1, y2 - y1, z2 - z1)
                translated_scanner = apply_translation(rotated_scanner, vector)
                if count_similarities(translated_scanner, ref) >= 12:
                    return translated_scanner
    raise RuntimeError


@cache
def compute_map() -> dict[tuple[int, int, int], int]:
    scanners = parse_scanners()
    grid = defaultdict(int)
    reference = scanners[0]
    for x, y, z in reference.beacons:
        grid[(x, y, z)] = -1
    grid[reference.location] = 1

    located_scanners = [reference]
    stack = scanners[1:]
    while stack:
        scanner = stack.pop(0)

        ref = get_neighbour_scanner(scanner, located_scanners)
        if ref is None:
            stack.append(scanner)
            continue

        rotated_scanner = find_rotation(scanner, ref)
        for x, y, z in rotated_scanner.beacons:
            grid[(x, y, z)] = -1
        grid[rotated_scanner.location] = 1

        located_scanners.append(rotated_scanner)
    return grid


def main1() -> int:
    grid = compute_map()
    return sum(1 for v in grid.values() if v == -1)


def main2() -> int:
    grid = compute_map()
    scanner_coordinates = [key for key, value in grid.items() if value > 0]
    max_length = 0
    for (x1, y1, z1), (x2, y2, z2) in itertools.combinations(scanner_coordinates, 2):
        length = abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1)
        max_length = max(max_length, length)
    return max_length
