from collections.abc import Iterator

from utils.parsing import parse_input


def parse_lines() -> Iterator[tuple[str, int]]:
    for line in parse_input():
        direction = line[0]
        count = int(line[1:])
        if count == 0:
            continue
        yield direction, count


def main1() -> int:
    res = 0
    index = 50
    for direction, count in parse_lines():
        if direction == "R":
            index = (index + count) % 100
        else:
            index = (index - count) % 100

        if index == 0:
            res += 1
    return res


def main2() -> int:
    res = 0
    index = 50
    for direction, count in parse_lines():
        if direction == "R":
            res += (index + count) // 100
            index = (index + count) % 100
        else:
            res += ((100 - index) % 100 + count) // 100
            index = (index - count) % 100
    return res
