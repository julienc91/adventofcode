from collections import defaultdict
from typing import Iterator


def parse_instructions() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def main1() -> int:
    res = 0
    for instruction in parse_instructions():
        if instruction.startswith("rect"):
            x, y = instruction.split()[1].split("x")
            res += int(x) * int(y)
    return res


def main2() -> str:
    grid: dict[tuple[int, int], bool] = defaultdict(bool)
    for instruction in parse_instructions():
        if instruction.startswith("rect"):
            x, y = map(int, instruction.split()[1].split("x"))
            for i in range(x):
                for j in range(y):
                    grid[(i, j)] = True
        elif instruction.startswith("rotate"):
            by = int(instruction.split()[-1])
            if instruction.startswith("rotate row"):
                y = int(instruction.split()[-3].split("=")[1])
                row = [grid[(i, y)] for i in range(50)]
                row = row[-by:] + row[:-by]
                for i in range(50):
                    grid[(i, y)] = row[i]
            elif instruction.startswith("rotate column"):
                x = int(instruction.split()[-3].split("=")[1])
                column = [grid[(x, i)] for i in range(6)]
                column = column[-by:] + column[:-by]
                for i in range(6):
                    grid[(x, i)] = column[i]
    for y in range(6):
        print("".join("#" if grid[(x, y)] else " " for x in range(50)))
    return "CFLELOYFCS"
