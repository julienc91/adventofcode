from functools import cache


@cache
def parse_instructions() -> list[str]:
    return input().strip().split(",")


def apply_instructions(data: str) -> str:
    data_list = list(data)
    for instruction in parse_instructions():
        if instruction.startswith("s"):
            i = int(instruction[1:])
            data_list = data_list[-i:] + data_list[:-i]
        elif instruction.startswith("x"):
            ia, ib = map(int, instruction[1:].split("/"))
            data_list[ia], data_list[ib] = data_list[ib], data_list[ia]
        elif instruction.startswith("p"):
            a, b = instruction[1:].split("/")
            ia, ib = data_list.index(a), data_list.index(b)
            data_list[ia], data_list[ib] = data_list[ib], data_list[ia]
        else:
            raise ValueError
    return "".join(data_list)


def main1() -> str:
    return apply_instructions("abcdefghijklmnop")


def main2() -> str:
    s = "abcdefghijklmnop"
    memory: dict[str, int] = {}
    indexes: list[str] = []

    counter = 0
    while s not in memory:
        memory[s] = counter
        indexes.append(s)

        s = apply_instructions(s)
        counter += 1

    loop_size = counter
    total_runs = 1_000_000_000
    return indexes[total_runs % loop_size]
