def parse_instructions() -> list[list[str]]:
    instructions: list[list[str]] = []
    try:
        while line := input().strip():
            instructions.append(line.replace(",", "").split())
    except EOFError:
        pass
    return instructions


def _main(register: dict[str, int]) -> int:
    instructions = parse_instructions()
    index = 0
    while True:
        try:
            instruction = instructions[index]
        except IndexError:
            break

        match instruction:
            case ["hlf", r]:
                register[r] //= 2
                index += 1
            case ["tpl", r]:
                register[r] *= 3
                index += 1
            case ["inc", r]:
                register[r] += 1
                index += 1
            case ["jmp", offset]:
                index += int(offset)
            case ["jie", r, offset]:
                if register[r] % 2 == 0:
                    index += int(offset)
                else:
                    index += 1
            case ["jio", r, offset]:
                if register[r] == 1:
                    index += int(offset)
                else:
                    index += 1
            case _:
                raise ValueError(f"Unknown instruction: {instruction}")
    return register["b"]


def main1() -> int:
    return _main({"a": 0, "b": 0})


def main2() -> int:
    return _main({"a": 1, "b": 0})
