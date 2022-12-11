def move(x: int, y: int, direction: str) -> tuple[int, int]:
    match direction:
        case "n":
            y += 1
        case "ne":
            x += 1
            y += 1 if x % 2 == 1 else 0
        case "nw":
            x -= 1
            y += 1 if x % 2 == 1 else 0
        case "s":
            y -= 1
        case "se":
            x += 1
            y -= 1 if x % 2 == 0 else 0
        case "sw":
            x -= 1
            y -= 1 if x % 2 == 0 else 0
        case _:
            raise ValueError()
    return x, y


def get_distance(x: int, y: int) -> int:
    return (abs(x) + 1) // 2 + abs(y)


def main1() -> int:
    directions = input().strip().split(",")
    x, y = 0, 0
    for direction in directions:
        x, y = move(x, y, direction)
    return get_distance(x, y)


def main2() -> int:
    directions = input().strip().split(",")
    x, y = 0, 0
    max_distance = 0
    for direction in directions:
        x, y = move(x, y, direction)
        max_distance = max(max_distance, get_distance(x, y))
    return max_distance
