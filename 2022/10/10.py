class Processor:
    CRT_WIDTH = 40

    def __init__(self) -> None:
        self.x = 1
        self.cycle = 0
        self.history: list[int] = [self.x]
        self.crt: list[bool] = []

    def process_input(self) -> None:
        try:
            while line := input().strip():
                self.add_instruction(line)
        except EOFError:
            pass

    def add_instruction(self, instruction: str) -> None:
        if instruction == "noop":
            self._increment_cycle()
        else:
            self._increment_cycle()
            self._increment_cycle()
            self.x += int(instruction.split()[1])

    def _increment_cycle(self) -> None:
        self.cycle += 1
        self.history.append(self.x)

        self.crt.append(abs(((self.cycle - 1) % self.CRT_WIDTH) - self.x) <= 1)

    def display(self) -> None:
        for i, value in enumerate(self.crt):
            if i > 0 and i % self.CRT_WIDTH == 0:
                print("", end="\n")
            print("#" if value else " ", end="")
        print("", end="\n")


def main1() -> int:
    processor = Processor()
    processor.process_input()

    cycles = [20, 60, 100, 140, 180, 220]
    return sum(processor.history[cycle] * cycle for cycle in cycles)


def main2() -> str:
    processor = Processor()
    processor.process_input()
    processor.display()
    return "EFUGLPAP"
