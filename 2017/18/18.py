from collections import defaultdict

from utils.parsing import parse_input


class ProgramPart1:
    def __init__(self, instructions: list[str], pid: int = 0):
        self.registries = defaultdict(int)
        self.pid = pid
        self.registries["p"] = pid
        self.index = 0
        self.instructions = instructions

        self.send_queue = []
        self.receive_queue = []
        self.waiting = False

    def _get_value(self, x: str) -> int:
        try:
            return int(x)
        except ValueError:
            return self.registries[x]

    def _handle_receive(self, x: str) -> None:
        if self._get_value(x) > 0:
            self.receive_queue.append(self.send_queue[-1])

    def _handle_send(self, x: str) -> None:
        self.send_queue.append(self._get_value(x))

    def execute(self) -> None:
        instruction = self.instructions[self.index]
        match instruction.split():
            case "snd", x:
                self._handle_send(x)
            case "set", x, y:
                self.registries[x] = self._get_value(y)
            case "add", x, y:
                self.registries[x] += self._get_value(y)
            case "mul", x, y:
                self.registries[x] *= self._get_value(y)
            case "mod", x, y:
                self.registries[x] %= self._get_value(y)
            case "rcv", x:
                self._handle_receive(x)
            case "jgz", x, y:
                if self._get_value(x) > 0:
                    jump = self._get_value(y)
                    self.index += jump - 1
            case _:
                raise ValueError(f"Unexpected instruction {instruction}")

        if not self.waiting:
            self.index += 1


class ProgramPart2(ProgramPart1):
    def _handle_receive(self, x: str) -> None:
        if not self.receive_queue:
            self.waiting = True
        else:
            self.registries[x] = self.receive_queue.pop(0)
            self.waiting = False


def main1() -> int:
    instructions = list(parse_input())
    program = ProgramPart1(instructions)
    while not program.receive_queue:
        program.execute()
    return program.receive_queue[0]


def main2() -> int:
    instructions = list(parse_input())
    count = 0
    program0 = ProgramPart2(instructions, pid=0)
    program1 = ProgramPart2(instructions, pid=1)

    while True:
        program0.execute()
        program1.execute()

        if program0.send_queue:
            program1.receive_queue.append(program0.send_queue.pop(0))
        if program1.send_queue:
            count += 1
            program0.receive_queue.append(program1.send_queue.pop(0))

        if (
            program0.waiting
            and program1.waiting
            and not program0.receive_queue
            and not program1.receive_queue
        ):
            break

    return count
