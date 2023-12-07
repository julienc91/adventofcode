from collections import Counter
from collections.abc import Iterator
from enum import Enum
from functools import cached_property
from typing import Self, TypeVar

from utils.parsing import parse_input


class HandTypes(Enum):
    FIVE_OF_A_KIND = (5,)
    FOUR_OF_A_KIND = (4, 1)
    FULL_HOUSE = (3, 2)
    THREE_OF_A_KIND = (3, 1, 1)
    TWO_PAIRS = (2, 2, 1)
    PAIR = (2, 1, 1, 1)
    HIGH_CARD = (1, 1, 1, 1, 1)


class Hand:
    _ordering = "23456789TJQKA"

    def __init__(self, cards: str, bid: int) -> None:
        self.cards = [self._ordering.index(card) for card in cards]
        self.bid = bid

    @cached_property
    def type(self) -> HandTypes:
        counter = sorted(Counter(self.cards).values(), reverse=True)
        return HandTypes(tuple(counter))

    def __lt__(self, other: Self) -> bool:
        return (self.type.value, self.cards) < (other.type.value, other.cards)


class HandWithJoker(Hand):
    _ordering = "J23456789TQKA"

    @cached_property
    def type(self) -> HandTypes:
        remaining_cards = [card for card in self.cards if card != 0]
        nb_jokers = len(self.cards) - len(remaining_cards)
        counter = sorted(Counter(remaining_cards).values(), reverse=True) or [0]
        counter[0] += nb_jokers
        return HandTypes(tuple(counter))


HandKlass = TypeVar("HandKlass", bound=Hand)


def parse_hands(hand_klass: type[HandKlass]) -> Iterator[HandKlass]:
    for line in parse_input():
        cards, bid = line.split()
        yield hand_klass(cards, bid=int(bid))


def _main(hand_klass: type[HandKlass]) -> int:
    hands = sorted(list(parse_hands(hand_klass)))
    return sum(hand.bid * rank for rank, hand in enumerate(hands, start=1))


def main1() -> int:
    return _main(Hand)


def main2() -> int:
    return _main(HandWithJoker)
