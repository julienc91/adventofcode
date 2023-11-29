from utils.parsing import parse_input


def parse_coordinates() -> set[tuple[int, int]]:
    coordinates = set()
    while line := input().strip():
        x, y = map(int, line.split(","))
        coordinates.add((x, y))
    return coordinates


def parse_instructions() -> list[tuple[str, int]]:
    instructions = []
    for line in parse_input():
        left, right = line.split("=")
        along = left[-1]
        instructions.append((along, int(right)))
    return instructions


def print_coordinates(coordinates: set[tuple[int, int]]) -> None:
    max_x = max(x for x, _ in coordinates) + 1
    max_y = max(y for _, y in coordinates) + 1
    grid = [["." for _ in range(max_x)] for _ in range(max_y)]
    for x, y in coordinates:
        grid[y][x] = "#"

    for line in grid:
        print("".join(line))


def do_fold(
    coordinates: set[tuple[int, int]], along: str, n: int
) -> set[tuple[int, int]]:
    if along not in ("x", "y"):
        raise ValueError(f"Unexpected value for along: {along}")

    new_coordinates = set()
    for x, y in coordinates:
        if along == "x" and x >= n:
            x = n - (x - n)
        elif along == "y" and y >= n:
            y = n - (y - n)
        new_coordinates.add((x, y))
    return new_coordinates


def main1() -> int:
    coordinates = parse_coordinates()
    instructions = parse_instructions()
    new_coordinates = do_fold(coordinates, *instructions[0])
    return len(new_coordinates)


def main2() -> int:
    coordinates = parse_coordinates()
    instructions = parse_instructions()
    for instruction in instructions:
        coordinates = do_fold(coordinates, *instruction)
    print_coordinates(coordinates)
    return -1
