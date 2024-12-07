from collections.abc import Iterator

from utils.parsing import parse_input

Equation = tuple[int, tuple[int, ...]]


def parse_equations() -> Iterator[Equation]:
    for line in parse_input():
        numbers = list(map(int, line.replace(":", "").split()))
        yield numbers[0], tuple(numbers[1:])


def is_valid(equation: Equation, with_combination: bool) -> bool:
    total, _ = equation

    def inner(*numbers: int) -> bool:
        match numbers:
            case (n,):
                return total == n
            case (a, *_) if total < a:
                return False
            case (a, b, *r):
                return (
                    inner(a + b, *r)
                    or inner(a * b, *r)
                    or (with_combination and inner(int(str(a) + str(b)), *r))
                )
            case _:
                raise ValueError()

    return inner(*equation[1])


def _main(with_combination: bool) -> int:
    res = 0
    for equation in parse_equations():
        if is_valid(equation, with_combination):
            total, _ = equation
            res += total
    return res


def main1() -> int:
    return _main(False)


def main2() -> int:
    return _main(True)
