from collections.abc import Iterator

from utils.parsing import parse_input


def execute(instructions: list[str], a: int) -> Iterator[int]:
    index = 0
    registries = {"a": a, "b": 0, "c": 0, "d": 0}

    while index < len(instructions):
        instruction = instructions[index]
        command, *args = instruction.split()
        match command:
            case "cpy":
                value = registries[args[0]] if args[0] in registries else int(args[0])
                registries[args[1]] = value
                index += 1
            case "inc":
                registries[args[0]] += 1
                index += 1
            case "dec":
                registries[args[0]] -= 1
                index += 1
            case "jnz":
                value = registries[args[0]] if args[0] in registries else int(args[0])
                if value != 0:
                    index += int(args[1])
                else:
                    index += 1
            case "out":
                value = registries[args[0]] if args[0] in registries else int(args[0])
                yield value
                index += 1
            case _:
                raise RuntimeError(f"Unknown command: {command}")


def main1() -> int:
    n = 0
    min_length = 10
    instructions = list(parse_input())

    while True:
        stack = []
        for i, value in enumerate(execute(instructions, n)):
            stack.append(value)
            if value not in (0, 1):
                break

            if value != i % 2:
                break

            if i >= min_length:
                return n

        n += 1


def main2() -> int:
    return -1
