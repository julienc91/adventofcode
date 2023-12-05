import re

from utils.parsing import parse_input


def parse_seeds() -> list[int]:
    seeds = list(map(int, re.findall(r"\d+", input())))
    input()
    return seeds


def parse_mappings() -> list[list[tuple[range, range]]]:
    mappings = []
    for _ in parse_input():
        ranges = []
        try:
            while line := input():
                destination_start, source_start, length = map(int, line.split())
                ranges.append(
                    (
                        range(destination_start, destination_start + length),
                        range(source_start, source_start + length),
                    )
                )
        except EOFError:
            pass
        mappings.append(ranges)

    return mappings


def find_corresponding_ranges(
    source: range, mapping: list[tuple[range, range]]
) -> list[range]:
    """
    Return the different ranges mapped to the given source range.
    """
    cursor = source.start
    corresponding_ranges = []
    mapping = sorted(mapping, key=lambda ranges: ranges[1].start)

    while cursor < source.stop:
        for to_range, from_range in mapping:
            if cursor < from_range.start:
                # Part of our range is not in the mapping: the corresponding range is the same as
                # the source range
                range_start = source.start
                range_end = min(source.stop, from_range.start) - 1
                corresponding_ranges.append(range(range_start, range_end + 1))
                cursor = from_range.start
            elif cursor in from_range:
                # Part of our range is in this mapping: the corresponding range is given by the mapping
                next_cursor = min(source.stop, from_range.stop)
                range_start = to_range.start + from_range.index(cursor)
                range_end = to_range.start + from_range.index(next_cursor - 1)
                corresponding_ranges.append(range(range_start, range_end + 1))
                cursor = next_cursor
            else:
                continue
            break
        else:
            # Our range is not in the mapping: the corresponding range is the same as the source range
            range_start = cursor
            range_end = source.stop
            corresponding_ranges.append(range(range_start, range_end + 1))
            break

    return corresponding_ranges


def _main(seed_ranges: list[range]) -> int:
    mappings = parse_mappings()

    source_ranges = seed_ranges

    while mappings:
        mapping = mappings.pop(0)
        next_ranges = []
        for source_range in source_ranges:
            next_ranges += find_corresponding_ranges(source_range, mapping)

        source_ranges = next_ranges

    return min(source_range.start for source_range in source_ranges)


def main1() -> int:
    seeds = parse_seeds()
    seed_ranges = [range(seed, seed + 1) for seed in seeds]
    return _main(seed_ranges)


def main2() -> int:
    seeds = parse_seeds()
    seed_ranges = [
        range(seeds[i], seeds[i] + seeds[i + 1]) for i in range(0, len(seeds), 2)
    ]
    return _main(seed_ranges)
