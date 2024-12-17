import re
from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Program:
    a: int
    b: int
    c: int

    instructions: list[int]
    cursor: int = 0

    def reset(self):
        self.a = 0
        self.b = 0
        self.c = 0
        self.cursor = 0

    def _get_combo_operand(self, operand: int) -> int:
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.a
        elif operand == 5:
            return self.b
        elif operand == 6:
            return self.c
        else:
            raise ValueError(operand)

    def _exec(self, instruction: int, operand: int) -> int | None:
        res = None
        if instruction == 0:
            self.a //= 2 ** self._get_combo_operand(operand)
        elif instruction == 1:
            self.b ^= operand
        elif instruction == 2:
            self.b = self._get_combo_operand(operand) % 8
        elif instruction == 3:
            if self.a != 0:
                self.cursor = operand - 2
        elif instruction == 4:
            self.b ^= self.c
        elif instruction == 5:
            res = self._get_combo_operand(operand) % 8
        elif instruction == 6:
            self.b = self.a // (2 ** self._get_combo_operand(operand))
        elif instruction == 7:
            self.c = self.a // (2 ** self._get_combo_operand(operand))
        else:
            raise ValueError(instruction)
        return res

    def run_step(self) -> int | None:
        instruction = self.instructions[self.cursor]
        operand = self.instructions[self.cursor + 1]
        res = self._exec(instruction, operand)
        self.cursor += 2
        return res

    def run(self) -> Iterator[int]:
        while self.cursor < len(self.instructions):
            res = self.run_step()
            if res is not None:
                yield res


def parse_data() -> Program:
    a = int(re.findall(r"\d+", input())[0])
    b = int(re.findall(r"\d+", input())[0])
    c = int(re.findall(r"\d+", input())[0])
    input()
    instructions = list(map(int, re.findall(r"\d+", input())))

    return Program(a, b, c, instructions)


def main1() -> str:
    program = parse_data()
    output = list(program.run())
    return ",".join(str(i) for i in output)


def main2() -> int:
    program = parse_data()
    queue = list(range(10))
    while queue:
        # Prog(8 * m + n) == (p, *Prog(m))
        a = queue.pop(0)
        program.reset()
        program.a = a
        res = list(program.run())
        if res == program.instructions:
            return a
        elif res == program.instructions[-len(res) :]:
            queue += [8 * a + i for i in range(10)]
    raise RuntimeError("Could not reverse program")
