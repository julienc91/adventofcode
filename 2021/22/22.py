import re
from collections.abc import Iterator

Cuboid = tuple[int, int, int, int, int, int]


def get_cuboid_area(cuboid: Cuboid) -> int:
    x0, x1, y0, y1, z0, z1 = cuboid
    return (x1 + 1 - x0) * (y1 + 1 - y0) * (z1 + 1 - z0)


def parse_instructions() -> Iterator[tuple[bool, Cuboid]]:
    line_format = re.compile(
        r"(on|off) x=(-?\d+)\.\.(-?\d+),y=(-?\d+)\.\.(-?\d+),z=(-?\d+)\.\.(-?\d+)"
    )
    try:
        while line := input().strip():
            match = line_format.search(line)
            assert match
            yield (
                match.group(1) == "on",
                (
                    int(match.group(2)),
                    int(match.group(3)),
                    int(match.group(4)),
                    int(match.group(5)),
                    int(match.group(6)),
                    int(match.group(7)),
                ),
            )
    except EOFError:
        pass


def has_intersection(c1: Cuboid, c2: Cuboid) -> bool:
    return (
        c1[1] >= c2[0]
        and c1[0] <= c2[1]
        and c1[3] >= c2[2]
        and c1[2] <= c2[3]
        and c1[5] >= c2[4]
        and c1[4] <= c2[5]
    )


def get_intersection(c1: Cuboid, c2: Cuboid) -> Cuboid | None:
    if not has_intersection(c1, c2):
        return None
    return (
        max(c1[0], c2[0]),
        min(c1[1], c2[1]),
        max(c1[2], c2[2]),
        min(c1[3], c2[3]),
        max(c1[4], c2[4]),
        min(c1[5], c2[5]),
    )


def restrict_area(cuboid: Cuboid, max_area: int) -> Cuboid | None:
    if max_area <= 0:
        return cuboid

    x0, x1, y0, y1, z0, z1 = cuboid

    def restrict_range(v0: int, v1: int) -> tuple[int, int] | None:
        if v0 > max_area or v1 < -max_area:
            return None
        if v0 < -max_area:
            v0 = -max_area
        if v1 > max_area:
            v1 = max_area
        return v0, v1

    x_range = restrict_range(x0, x1)
    y_range = restrict_range(y0, y1)
    z_range = restrict_range(z0, z1)
    if x_range is None or y_range is None or z_range is None:
        return None

    return x_range[0], x_range[1], y_range[0], y_range[1], z_range[0], z_range[1]


def apply_instruction(
    cuboids: list[tuple[Cuboid, bool]],
    on: bool,
    cuboid: Cuboid,
    max_area: int,
) -> None:
    restricted_cuboid = restrict_area(cuboid, max_area)
    if restricted_cuboid is None:
        return

    cuboid = restricted_cuboid
    intersections: list[Cuboid] = []
    splits: list[Cuboid] = []

    for ref_cuboid, ref_on in cuboids:
        intersection = get_intersection(cuboid, ref_cuboid)
        if intersection is not None:
            if ref_on:
                intersections.append(intersection)
            else:
                splits.append(intersection)

    cuboids.extend([(intersection, True) for intersection in splits])
    cuboids.extend([(intersection, False) for intersection in intersections])
    if on:
        cuboids.append((cuboid, True))


def _main(max_area: int = 0) -> int:
    cuboids: list[tuple[Cuboid, bool]] = []
    for instruction in parse_instructions():
        apply_instruction(cuboids, *instruction, max_area=max_area)
    return sum(get_cuboid_area(cuboid) * (1 if on else -1) for cuboid, on in cuboids)


def main1() -> int:
    return _main(50)


def main2() -> int:
    return _main()
