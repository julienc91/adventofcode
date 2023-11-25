from collections.abc import Iterator


def parse_directions() -> Iterator[str]:
    yield from input()


def main1() -> int:
    x, y = 0, 0
    visited: set[tuple[int, int]] = {(x, y)}
    for direction in parse_directions():
        if direction == ">":
            x += 1
        elif direction == "<":
            x -= 1
        elif direction == "^":
            y -= 1
        elif direction == "v":
            y += 1
        visited.add((x, y))
    return len(visited)


def main2() -> int:
    x1, y1 = 0, 0
    x2, y2 = 0, 0
    visited: set[tuple[int, int]] = {(x1, y1)}
    is_robot = False
    for direction in parse_directions():
        x, y = (x2, y2) if is_robot else (x1, y1)
        if direction == ">":
            x += 1
        elif direction == "<":
            x -= 1
        elif direction == "^":
            y -= 1
        elif direction == "v":
            y += 1
        visited.add((x, y))

        if is_robot:
            x2, y2 = x, y
        else:
            x1, y1 = x, y
        is_robot = not is_robot
    return len(visited)
