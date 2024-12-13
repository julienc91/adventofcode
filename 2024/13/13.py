import re
from collections.abc import Iterator


def parse_problems() -> Iterator[tuple[int, int, int, int, int, int]]:
    try:
        while True:
            a, b = map(int, re.findall(r"(\d+)", input()))
            c, d = map(int, re.findall(r"(\d+)", input()))
            x, y = map(int, re.findall(r"(\d+)", input()))
            yield a, b, c, d, x, y
            input()
    except EOFError:
        pass


def solve_problem(a: int, b: int, c: int, d: int, x: int, y: int) -> tuple[int, int]:
    n = (y * a - b * x) / (-b * c + d * a)
    m = (x - n * c) / a
    if n.is_integer() and m.is_integer():
        return int(m), int(n)
    raise ValueError("Cannot be solved")


def main1() -> int:
    total = 0
    for problem in parse_problems():
        try:
            m, n = solve_problem(*problem)
        except ValueError:
            continue

        if m <= 100 and n <= 100:
            total += m * 3 + n * 1
    return total


def main2() -> int:
    total = 0
    for a, b, c, d, x, y in parse_problems():
        x += 10000000000000
        y += 10000000000000
        try:
            m, n = solve_problem(a, b, c, d, x, y)
        except ValueError:
            continue

        total += m * 3 + n * 1
    return total
