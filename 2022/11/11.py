from collections.abc import Callable
from dataclasses import dataclass


@dataclass
class Item:
    worry_level: int


@dataclass
class Monkey:
    id: int
    items: list[Item]
    inspection_func: Callable[[Item], int]
    test_divisible_by: int
    throw_targets: tuple[int, int]
    with_worry_relief: bool

    monkeys_by_id: list["Monkey"] | None = None
    common_factor: int = 0
    count_inspections: int = 0

    def throw_item(self) -> None:
        item = self.items.pop(0)
        if item.worry_level % self.test_divisible_by == 0:
            target_id = self.throw_targets[0]
        else:
            target_id = self.throw_targets[1]

        target = (self.monkeys_by_id or [])[target_id]
        target.items.append(item)

    def inspect_item(self) -> None:
        item = self.items[0]
        item.worry_level = self.inspection_func(item)
        if self.with_worry_relief:
            item.worry_level //= 3
        item.worry_level %= self.common_factor
        self.count_inspections += 1

    def play_turn(self) -> None:
        while self.items:
            self.inspect_item()
            self.throw_item()


def parse_monkey(with_worry_relief: bool) -> Monkey:
    monkey_id = int(input().strip().split()[-1][:-1])
    items_worry_levels = map(int, input().strip().split(": ")[1].split(", "))

    inspection_details = input().strip().split()
    inspection_operation: Callable[[int, int], int] = {
        "+": lambda a, b: a + b,
        "*": lambda a, b: a * b,
    }[inspection_details[-2]]
    inspection_factor = inspection_details[-1]

    test_divisible_by = int(input().strip().split()[-1])
    throw_targets = (
        int(input().strip().split()[-1]),
        int(input().strip().split()[-1]),
    )

    items = [Item(worry_level=worry_level) for worry_level in items_worry_levels]
    return Monkey(
        id=monkey_id,
        items=items,
        inspection_func=lambda item: inspection_operation(
            item.worry_level,
            item.worry_level if inspection_factor == "old" else int(inspection_factor),
        ),
        test_divisible_by=test_divisible_by,
        throw_targets=throw_targets,
        with_worry_relief=with_worry_relief,
    )


def parse_input(with_worry_relief: bool) -> list[Monkey]:
    game: list[Monkey] = []
    common_factor = 3
    try:
        while True:
            monkey = parse_monkey(with_worry_relief)
            monkey.monkeys_by_id = game
            common_factor *= monkey.test_divisible_by
            game.append(monkey)
            input()
    except EOFError:
        pass
    for monkey in game:
        monkey.common_factor = common_factor
    return game


def _main(nb_rounds: int, with_worry_relief: bool) -> int:
    game = parse_input(with_worry_relief=with_worry_relief)
    for _ in range(nb_rounds):
        for monkey in game:
            monkey.play_turn()

    nb_inspections = sorted([monkey.count_inspections for monkey in game], reverse=True)
    return nb_inspections[0] * nb_inspections[1]


def main1() -> int:
    return _main(20, True)


def main2() -> int:
    return _main(10_000, False)
