from dataclasses import dataclass
from typing import Iterator


@dataclass
class Bot:
    name: str
    chips: tuple[int, int] = (0, 0)
    instruction: tuple[str, str] = ("", "")

    @property
    def is_active(self) -> bool:
        return self.chips[0] != 0 and self.chips[1] != 0

    def receive_value(self, value: int) -> None:
        if self.chips[0] == 0 and self.chips[1] == 0:
            self.chips = (value, 0)
        else:
            self.chips = (min(value, self.chips[0]), max(value, self.chips[0]))

    def set_instruction(self, lower_output: str, higher_output: str) -> None:
        self.instruction = (lower_output, higher_output)

    def execute_instruction(self, all_bots: dict[str, "Bot"]) -> None:
        lower_value, high_value = sorted(self.chips)
        all_bots[self.instruction[0]].receive_value(lower_value)
        all_bots[self.instruction[1]].receive_value(high_value)
        self.chips = (0, 0)


def parse_instructions() -> Iterator[str]:
    try:
        while line := input().strip():
            yield line
    except EOFError:
        pass


def setup_bots() -> dict[str, Bot]:
    all_bots: dict[str, Bot] = {}
    for line in parse_instructions():
        if line.startswith("value"):
            _, value, _, _, _, bot_name = line.split()
            bot_name = f"bot_{bot_name}"
            if bot_name not in all_bots:
                all_bots[bot_name] = Bot(bot_name)
            all_bots[bot_name].receive_value(int(value))
        elif line.startswith("bot"):
            (
                _,
                sender,
                _,
                _,
                _,
                receiver_low_type,
                receiver_low,
                _,
                _,
                _,
                receiver_high_type,
                receiver_high,
            ) = line.split()
            sender = f"bot_{sender}"
            if sender not in all_bots:
                all_bots[sender] = Bot(sender)

            receiver_low = f"{receiver_low_type}_{receiver_low}"
            if receiver_low not in all_bots:
                all_bots[receiver_low] = Bot(receiver_low)

            receiver_high = f"{receiver_high_type}_{receiver_high}"
            if receiver_high not in all_bots:
                all_bots[receiver_high] = Bot(receiver_high)

            all_bots[sender].set_instruction(receiver_low, receiver_high)
    return all_bots


def main1() -> int:
    all_bots = setup_bots()
    while True:
        for bot in all_bots.values():
            if not bot.is_active:
                continue
            if bot.name.startswith("output"):
                continue

            if bot.chips == (17, 61):
                return int(bot.name.split("_")[1])
            bot.execute_instruction(all_bots)
            break


def main2() -> int:
    all_bots = setup_bots()
    while True:
        for bot in all_bots.values():
            if not bot.is_active:
                continue
            if bot.name.startswith("output"):
                continue

            bot.execute_instruction(all_bots)
            break
        else:
            break
    return (
        all_bots["output_0"].chips[0]
        * all_bots["output_1"].chips[0]
        * all_bots["output_2"].chips[0]
    )
