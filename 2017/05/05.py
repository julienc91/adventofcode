from collections.abc import Callable

from utils.parsing import parse_input


def _main(increment: Callable[[int], int]) -> int:
    index, counter = 0, 0
    instructions = list(parse_input(int))
    try:
        while True:
            value = instructions[index]
            instructions[index] = increment(value)
            index += value
            counter += 1
    except IndexError:
        pass
    return counter


def main1() -> int:
    return _main(lambda value: value + 1)


def main2() -> int:
    return _main(lambda value: value + (-1 if value >= 3 else 1))
