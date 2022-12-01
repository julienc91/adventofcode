from collections.abc import Iterator


def parse_instructions() -> Iterator[str]:
    yield from input()


def main1() -> int:
    res = 0
    for c in parse_instructions():
        res = res + (1 if c == "(" else -1)
    return res


def main2() -> int:
    res = 0
    for i, c in enumerate(parse_instructions(), start=1):
        res = res + (1 if c == "(" else -1)
        if res == -1:
            return i
    return -1
