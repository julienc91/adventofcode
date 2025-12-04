from utils.parsing import parse_input


def parse_paper_locations() -> set[tuple[int, int]]:
    locations = set()
    for y, line in enumerate(parse_input()):
        for x, value in enumerate(line):
            if value == "@":
                locations.add((x, y))
    return locations


def is_accessible(x: int, y: int, paper_locations: set[tuple[int, int]]) -> int:
    count = 0
    for dx, dy in [
        (-1, -1),
        (-1, 0),
        (-1, 1),
        (0, -1),
        (0, 1),
        (1, -1),
        (1, 0),
        (1, 1),
    ]:
        if (x + dx, y + dy) in paper_locations:
            count += 1
            if count >= 4:
                return False
    return True


def main1() -> int:
    paper_locations = parse_paper_locations()
    return sum(is_accessible(x, y, paper_locations) for x, y in paper_locations)


def main2() -> int:
    paper_locations = parse_paper_locations()
    locations_count = len(paper_locations)

    while True:
        locations_to_remove = set()
        for x, y in paper_locations:
            if is_accessible(x, y, paper_locations):
                locations_to_remove.add((x, y))

        paper_locations -= locations_to_remove
        if not locations_to_remove:
            break

    return locations_count - len(paper_locations)
