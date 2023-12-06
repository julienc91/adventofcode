import math
import re


def parse_races() -> list[tuple[int, int]]:
    times = list(map(int, re.findall(r"\d+", input())))
    distances = list(map(int, re.findall(r"\d+", input())))
    return [(t, d) for t, d in zip(times, distances)]


def parse_race() -> tuple[int, int]:
    times = int("".join(re.findall(r"\d+", input())))
    distances = int("".join(re.findall(r"\d+", input())))
    return times, distances


def process_race(time: int, distance: int) -> int:
    # Compute solutions of x * (time - x) > longest_distance
    min_range = math.ceil(0.5 * (time - math.sqrt(time * time - 4 * distance)))
    max_range = math.floor(0.5 * (time + math.sqrt(time * time - 4 * distance)))
    return max_range - min_range + 1


def main1() -> int:
    races = parse_races()
    return math.prod(process_race(time, distance) for time, distance in races)


def main2() -> int:
    time, distance = parse_race()
    return process_race(time, distance)
