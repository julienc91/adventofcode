from collections.abc import Callable, Iterator


def parse_input() -> list[list[str]]:
    nb_stacks = 9
    stack_input_length = 4
    stacks: list[list[str]] = [[] for _ in range(nb_stacks)]
    while line := input().rstrip():
        for i in range(1, nb_stacks * stack_input_length, stack_input_length):
            char = line[i]
            if char == " ":
                continue
            elif char.isdigit():
                continue
            else:
                stacks[i // stack_input_length].append(char)
    return stacks


def parse_instructions() -> Iterator[tuple[int, int, int]]:
    try:
        while line := input().strip():
            elements = line.split()
            yield int(elements[1]), int(elements[3]), int(elements[5])
    except EOFError:
        pass


def cratemover_9000(stacks: list[list[str]], instruction: tuple[int, int, int]) -> None:
    count, start, end = instruction[0], instruction[1] - 1, instruction[2] - 1
    for _ in range(count):
        value = stacks[start].pop(0)
        stacks[end].insert(0, value)


def cratemover_9001(stacks: list[list[str]], instruction: tuple[int, int, int]) -> None:
    count, start, end = instruction[0], instruction[1] - 1, instruction[2] - 1
    value = [stacks[start].pop(0) for _ in range(count)]
    stacks[end] = value + stacks[end]


def _main(
    apply_instruction: Callable[[list[list[str]], tuple[int, int, int]], None]
) -> str:
    stacks = parse_input()
    for instruction in parse_instructions():
        apply_instruction(stacks, instruction)
    return "".join(stack[0] for stack in stacks if stack)


def main1() -> str:
    return _main(cratemover_9000)


def main2() -> str:
    return _main(cratemover_9001)
