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


def process_race(time: int, longest_distance: int) -> int:
    count_wins = 0
    for hold_duration in range(time + 1):
        speed = hold_duration
        distance = speed * (time - hold_duration)
        if distance > longest_distance:
            count_wins += 1
    return count_wins


def process_race_v2(time: int, longest_distance: int) -> int:
    left_cursor = time // 2
    while True:
        speed = hold_duration = left_cursor
        distance = speed * (time - hold_duration)






def main1() -> int:
    races = parse_races()
    return math.prod(process_race(time, distance) for time, distance in races)


def main2() -> int:
    race = parse_race()
    print(race)
