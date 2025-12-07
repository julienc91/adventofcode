from collections import defaultdict

from utils.parsing import parse_input


def parse_grid() -> tuple[tuple[int, int], set[tuple[int, int]], int]:
    first_line = input()
    start = (first_line.index("S"), 0)

    splitter_locations = set()
    max_y = 0
    for y, line in enumerate(parse_input(), start=1):
        max_y = y
        for x, c in enumerate(line):
            if c == "^":
                splitter_locations.add((x, y))

    return start, splitter_locations, max_y


def main1() -> int:
    start, splitter_locations, max_y = parse_grid()
    beam_locations = {start}
    count_split = 0
    while beam_locations:
        next_beam_locations = set()
        for x, y in beam_locations:
            x2, y2 = x, y + 1
            if y2 > max_y:
                continue

            if (x2, y2) not in splitter_locations:
                next_beam_locations.add((x2, y2))
            else:
                count_split += 1
                next_beam_locations.add((x2 - 1, y2))
                next_beam_locations.add((x2 + 1, y2))
        beam_locations = next_beam_locations
    return count_split


def main2() -> int:
    start, splitter_locations, max_y = parse_grid()
    beam_locations = {start: 1}
    count_timelines = 1
    while beam_locations:
        next_beam_locations = defaultdict(int)
        for (x, y), count in beam_locations.items():
            x2, y2 = x, y + 1
            if y2 > max_y:
                continue

            if (x2, y2) not in splitter_locations:
                next_beam_locations[(x2, y2)] += count
            else:
                count_timelines += count
                next_beam_locations[(x2 - 1, y2)] += count
                next_beam_locations[(x2 + 1, y2)] += count
        beam_locations = next_beam_locations
    return count_timelines
