import itertools
import re
from dataclasses import dataclass

from utils.parsing import parse_input


@dataclass(frozen=True)
class Coordinates:
    x: float
    y: float
    z: float

    def __add__(self, other: "Coordinates") -> "Coordinates":
        return Coordinates(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other: "Coordinates") -> "Coordinates":
        return Coordinates(self.x - other.x, self.y - other.y, self.z - other.z)

    def __neg__(self) -> "Coordinates":
        return Coordinates(-self.x, -self.y, -self.z)

    def __mul__(self, other: float) -> "Coordinates":
        return Coordinates(self.x * other, self.y * other, self.z * other)

    def __truediv__(self, other: float) -> "Coordinates":
        return Coordinates(self.x / other, self.y / other, self.z / other)


@dataclass
class Hailstone:
    coordinates: Coordinates
    velocity: Coordinates


def parse_hailstones() -> list[Hailstone]:
    res = []
    for line in parse_input():
        x, y, z, dx, dy, dz = map(int, re.findall(r"-?\d+", line))
        res.append(Hailstone(Coordinates(x, y, z), Coordinates(dx, dy, dz)))
    return res


def main1():
    hailstones = parse_hailstones()
    min_c, max_c = 200_000_000_000_000, 400_000_000_000_000
    res = 0
    for a, b in itertools.combinations(hailstones, 2):
        a_slope = a.velocity.y / a.velocity.x
        b_slope = b.velocity.y / b.velocity.x
        if a_slope == b_slope:
            continue

        cx = (
            (a.coordinates.y - a_slope * a.coordinates.x)
            - (b.coordinates.y - b_slope * b.coordinates.x)
        ) / (b_slope - a_slope)
        cy = a_slope * (cx - a.coordinates.x) + a.coordinates.y

        if ((cx >= a.coordinates.x) != (a.velocity.x >= 0)) or (
            (cx >= b.coordinates.x) != (b.velocity.x >= 0)
        ):
            continue
        if min_c <= cx <= max_c and min_c <= cy <= max_c:
            res += 1
    return res


def vector_product(a: Coordinates, b: Coordinates) -> Coordinates:
    return Coordinates(
        x=a.y * b.z - a.z * b.y,
        y=a.z * b.x - a.x * b.z,
        z=a.x * b.y - a.y * b.x,
    )


def scalar_product(a: Coordinates, b: Coordinates) -> float:
    return a.x * b.x + a.y * b.y + a.z * b.z


def intersection(plane: Coordinates, hailstone: Hailstone) -> tuple[Coordinates, float]:
    u = scalar_product(plane, -hailstone.coordinates)
    v = scalar_product(plane, hailstone.velocity)
    t = u / v
    return hailstone.coordinates + hailstone.velocity * t, t


def main2():
    """
    Implemented from u/Crazy_Marx 's idea
    https://www.reddit.com/r/adventofcode/comments/18qexvu/2023_day_24_part_2_3d_vector_interpretation_and/
    """
    hailstones = parse_hailstones()
    h0, h1, h2, h3, *_ = hailstones  # Only 4 hailstones are needed

    # Translate everything to h0's reference
    translated_hailstones = []
    for h in (h1, h2, h3):
        translated_hailstones.append(
            Hailstone(
                coordinates=h.coordinates - h0.coordinates,
                velocity=h.velocity - h0.velocity,
            )
        )

    h1, h2, h3 = translated_hailstones
    n = vector_product(h1.coordinates, h1.coordinates + h1.velocity)

    p2, t2 = intersection(n, h2)
    p3, t3 = intersection(n, h3)

    velocity = (p3 - p2) / (t3 - t2)
    coordinates = p2 - (velocity * t2)
    rock = Hailstone(coordinates, velocity)

    # Translate back to the original coordinates
    rock = Hailstone(rock.coordinates + h0.coordinates, rock.velocity + h0.velocity)
    return int(round(rock.coordinates.x + rock.coordinates.y + rock.coordinates.z))
