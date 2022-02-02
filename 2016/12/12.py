def parse_instructions() -> list[str]:
    res: list[str] = []
    try:
        while line := input().strip():
            res.append(line)
    except EOFError:
        pass
    return res


def _main(registries: dict[str, int]) -> int:
    instructions = parse_instructions()
    index = 0

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
    return registries["a"]


def main1() -> int:
    return _main({"a": 0, "b": 0, "c": 0, "d": 0})


def main2() -> int:
    return _main({"a": 0, "b": 0, "c": 1, "d": 0})
