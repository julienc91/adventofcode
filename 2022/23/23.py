from enum import Enum


class Direction(Enum):
    NORTH = "N"
    SOUTH = "S"
    WEST = "W"
    EAST = "E"


def parse_input() -> set[tuple[int, int]]:
    elves_locations: set[tuple[int, int]] = set()
    try:
        y = 0
        while line := input().strip():
            for x, c in enumerate(line):
                if c == "#":
                    elves_locations.add((x, y))
            y += 1
    except EOFError:
        pass
    return elves_locations


def get_neighbours(
    x: int, y: int, locations: set[tuple[int, int]]
) -> dict[Direction, bool]:
    res = {
        Direction.NORTH: False,
        Direction.SOUTH: False,
        Direction.WEST: False,
        Direction.EAST: False,
    }
    for x2, y2 in [(x - 1, y - 1), (x, y - 1), (x + 1, y - 1)]:
        if (x2, y2) in locations:
            res[Direction.NORTH] = True
            break

    for x2, y2 in [(x - 1, y + 1), (x, y + 1), (x + 1, y + 1)]:
        if (x2, y2) in locations:
            res[Direction.SOUTH] = True
            break

    for x2, y2 in [(x - 1, y - 1), (x - 1, y), (x - 1, y + 1)]:
        if (x2, y2) in locations:
            res[Direction.WEST] = True
            break

    for x2, y2 in [(x + 1, y + 1), (x + 1, y), (x + 1, y - 1)]:
        if (x2, y2) in locations:
            res[Direction.EAST] = True
            break

    return res


def _main(nb_turns: int | None) -> tuple[int, int]:
    locations = parse_input()
    nb_elves = len(locations)
    i = 0
    while nb_turns is None or i < nb_turns:
        directions = list(Direction)

        proposed_moves: dict[tuple[int, int], tuple[int, int]] = {}
        denied_moves: set[tuple[int, int]] = set()

        for x, y in locations:
            neighbours = get_neighbours(x, y, locations)
            if not any(neighbours.values()):
                continue

            for j in range(len(directions)):
                direction = directions[(i + j) % len(directions)]
                if neighbours[direction]:
                    continue

                if direction == Direction.NORTH:
                    x2, y2 = x, y - 1
                elif direction == Direction.SOUTH:
                    x2, y2 = x, y + 1
                elif direction == Direction.WEST:
                    x2, y2 = x - 1, y
                elif direction == Direction.EAST:
                    x2, y2 = x + 1, y
                else:
                    raise ValueError

                if (x2, y2) in proposed_moves:
                    denied_moves.add((x2, y2))
                else:
                    proposed_moves[(x2, y2)] = (x, y)
                break

        has_moved_at_least_one = False
        for x, y in proposed_moves:
            if (x, y) in denied_moves:
                continue

            has_moved_at_least_one = True
            previous_x, previous_y = proposed_moves[(x, y)]
            locations.remove((previous_x, previous_y))
            locations.add((x, y))

        i += 1
        if not has_moved_at_least_one:
            break

    min_x = min(x for x, _ in locations)
    max_x = max(x for x, _ in locations)
    min_y = min(y for _, y in locations)
    max_y = max(y for _, y in locations)

    return i, abs(max_x + 1 - min_x) * abs(max_y + 1 - min_y) - nb_elves


def main1() -> int:
    turn, count = _main(10)
    return count


def main2() -> int:
    turn, _ = _main(None)
    return turn
