from collections.abc import Iterator
from functools import cached_property

from utils.parsing import parse_input


class Card:
    def __init__(self, line: str) -> None:
        line = line.split(":")[1]
        left, right = line.split("|")

        self.winning_numbers = set(map(int, left.split()))
        self.owned_numbers = set(map(int, right.split()))
        self.count = 1

    @cached_property
    def nb_correct(self) -> int:
        return len(self.winning_numbers & self.owned_numbers)


def parse_cards() -> Iterator[Card]:
    for line in parse_input():
        yield Card(line)


def main1() -> int:
    points = 0
    for card in parse_cards():
        if card.nb_correct > 0:
            points += 2 ** (card.nb_correct - 1)
    return points


def main2() -> int:
    cards = list(parse_cards())
    for i, card in enumerate(cards):
        nb_correct = card.nb_correct
        for other_card in cards[i + 1 : i + 1 + nb_correct]:
            other_card.count += card.count

    return sum(card.count for card in cards)
