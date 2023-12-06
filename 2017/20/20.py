import re
from collections import defaultdict
from dataclasses import dataclass

from utils.parsing import parse_input


@dataclass
class Vector:
    x: int
    y: int
    z: int


@dataclass
class Particle:
    position: Vector
    speed: Vector
    acceleration: Vector

    def tick(self) -> None:
        self.speed.x += self.acceleration.x
        self.speed.y += self.acceleration.y
        self.speed.z += self.acceleration.z

        self.position.x += self.speed.x
        self.position.y += self.speed.y
        self.position.z += self.speed.z

    @property
    def coordinates(self) -> tuple[int, int, int]:
        return self.position.x, self.position.y, self.position.z


def parse_particles() -> list[Particle]:
    particles = []
    for line in parse_input():
        numbers = re.findall(r"(-?\d+)", line)
        x, y, z, vx, vy, vz, ax, ay, az = map(int, numbers)
        particle = Particle(Vector(x, y, z), Vector(vx, vy, vz), Vector(ax, ay, az))
        particles.append(particle)
    return particles


def main1() -> int:
    res = -1
    lowest_acceleration = -1
    for i, particle in enumerate(parse_particles()):
        va = particle.acceleration
        acceleration = abs(va.x) + abs(va.y) + abs(va.z)
        if lowest_acceleration < 0 or lowest_acceleration > acceleration:
            lowest_acceleration = acceleration
            res = i
    return res


def apply_tick(particles: list[Particle]) -> list[Particle]:
    particles_by_position = defaultdict(list)
    for particle in particles:
        particle.tick()
        particles_by_position[particle.coordinates].append(particle)

    return [
        particles[0]
        for particles in particles_by_position.values()
        if len(particles) == 1
    ]


def main2() -> int:
    particles = parse_particles()
    for _ in range(50):  # arbitrary
        particles = apply_tick(particles)
    return len(particles)
