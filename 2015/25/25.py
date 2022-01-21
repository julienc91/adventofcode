import re


def parse_coordinates() -> tuple[int, int]:
    instruction = input()

    match = re.search(r"column (\d+)", instruction)
    assert match
    x = int(match.group(1))

    match = re.search(r"row (\d+)", instruction)
    assert match
    y = int(match.group(1))

    return x, y


def get_next_code(current_code: int) -> int:
    return (current_code * 252533) % 33554393


def main1() -> int:
    x, y = parse_coordinates()
    a, b = 1, 1
    current_diag = 1

    code = 20151125
    while (a, b) != (x, y):
        if b > 1:
            a += 1
            b -= 1
        else:
            current_diag += 1
            a = 1
            b = current_diag
        code = get_next_code(code)
    return code


def main2() -> int:
    return -1
