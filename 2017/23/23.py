import re
from collections import defaultdict

from utils.parsing import parse_input


class Program:
    def __init__(self, instructions: list[str]):
        self.registries = defaultdict(int)
        self.index = 0
        self.count = 0
        self.instructions = instructions

    def _get_value(self, x: str) -> int:
        try:
            return int(x)
        except ValueError:
            return self.registries[x]

    def execute_step(self) -> None:
        instruction = self.instructions[self.index]
        match instruction.split():
            case "set", x, y:
                self.registries[x] = self._get_value(y)
            case "sub", x, y:
                self.registries[x] -= self._get_value(y)
            case "mul", x, y:
                self.registries[x] *= self._get_value(y)
                self.count += 1
            case "jnz", x, y:
                if self._get_value(x) != 0:
                    jump = self._get_value(y)
                    self.index += jump - 1
            case _:
                raise ValueError(f"Unexpected instruction {instruction}")

        self.index += 1

    def execute(self) -> None:
        while self.index < len(self.instructions):
            self.execute_step()


def main1() -> int:
    instructions = list(parse_input())
    program = Program(instructions)
    program.execute()
    return program.count


def is_prime(n):
    for a in range(2, int(n**0.5) + 1):
        if n % a == 0:
            return False
    return True


def main2() -> int:
    factor = int(re.findall(r"\d+", input())[0])
    count = 0
    start = factor * 100 + 100_000
    for n in range(start, start + 17_001, 17):
        if not is_prime(n):
            count += 1
    return count


"""
b = 99 * 100 + 100000
c = b + 17000
count = 0
while True:
    f = 1
    d = 2
    while True:
        e = 2
        while True:
            g = d * e - b
            if g == 0:
                f = 0
            e += 1
            g = e - b
            if g == 0:
                break
        d += 1
        if d == b:
            break
    if f == 0:
        count += 1
    if b == c:
        return
    b += 17
"""
