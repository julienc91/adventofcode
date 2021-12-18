import re


def parse_input() -> tuple[tuple[int, int], tuple[int, int]]:
    line = input().strip()
    search = re.search(r"x=(\d+)..(\d+), y=(-\d+)..(-\d+)", line)
    assert search
    x_range = (int(search.group(1)), int(search.group(2)))
    y_range = (int(search.group(3)), int(search.group(4)))
    return x_range, y_range


def is_target_hit(
    x_velocity: int, y_velocity: int, x_range: tuple[int, int], y_range: tuple[int, int]
) -> bool:
    x, y = 0, 0
    while True:
        x += x_velocity
        y += y_velocity

        x_velocity = max(x_velocity - 1, 0)
        y_velocity -= 1

        is_in_target = (x_range[0] <= x <= x_range[1]) and (
            y_range[0] <= y <= y_range[1]
        )
        if is_in_target:
            return True

        if x > x_range[1]:
            return False
        elif x < x_range[0] and x_velocity <= 0:
            return False
        elif y < y_range[0] and y_velocity <= 0:
            return False


def get_max_y(y_range: tuple[int, int]) -> int:
    v = -y_range[0] - 1
    return v * (v + 1) // 2


def main1() -> int:
    _, y_range = parse_input()
    return get_max_y(y_range)


def main2() -> int:
    x_range, y_range = parse_input()
    max_y = get_max_y(y_range)
    count = 0
    for x in range(0, x_range[1] + 1):
        for y in range(y_range[0], 2 * int(max_y ** 0.5)):
            if is_target_hit(x, y, x_range, y_range):
                count += 1
    return count
