import math

from utils.parsing import parse_input


def toggle_instruction(instruction: str) -> str:
    command, *args = instruction.split()
    if len(args) == 1:
        if command == "inc":
            return instruction.replace("inc ", "dec ")
        return instruction.replace(f"{command} ", "inc ")
    if command == "jnz":
        return instruction.replace("jnz ", "cpy ")
    return instruction.replace(f"{command} ", "jnz ")


def _main(registries: dict[str, int]) -> int:
    instructions = list(parse_input())
    index = 0

    while index < len(instructions):
        instruction = instructions[index]
        command, *args = instruction.split()
        match command:
            case "tgl":
                value = registries[args[0]] if args[0] in registries else int(args[0])
                if 0 <= index + value < len(instructions):
                    instructions[index + value] = toggle_instruction(
                        instructions[index + value]
                    )
                index += 1
            case "cpy":
                value = registries[args[0]] if args[0] in registries else int(args[0])
                if args[1] in registries:
                    registries[args[1]] = value
                index += 1
            case "inc":
                if args[0] in registries:
                    registries[args[0]] += 1
                index += 1
            case "dec":
                if args[0] in registries:
                    registries[args[0]] -= 1
                index += 1
            case "jnz":
                value = registries[args[0]] if args[0] in registries else int(args[0])
                jmp = registries[args[1]] if args[1] in registries else int(args[1])
                if value != 0:
                    index += jmp
                else:
                    index += 1

    return registries["a"]


def main1() -> int:
    return _main({"a": 7, "b": 0, "c": 0, "d": 0})


def main2() -> int:
    # 6: 8196 = 6! + 7476
    # 7: 12516 = 7! + 7476
    # 8: 47796 = 8! + 7476
    # 9: 370356 = 9! + 7476
    # ...
    return math.factorial(12) + 7476
