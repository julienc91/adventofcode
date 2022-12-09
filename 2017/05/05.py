from collections.abc import Callable


def get_instructions() -> list[int]:
    instructions: list[int] = []
    try:
        while line := input().strip():
            instructions.append(int(line))
    except EOFError:
        pass
    return instructions


def _main(increment: Callable[[int], int]) -> int:
    index, counter = 0, 0
    instructions = get_instructions()
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
