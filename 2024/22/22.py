from collections import defaultdict, deque
from collections.abc import Iterator

from utils.parsing import parse_input


def iterate(secret_number) -> Iterator[int]:
    yield secret_number
    while True:
        secret_number = ((secret_number << 6) ^ secret_number) % 16777216
        secret_number = ((secret_number >> 5) ^ secret_number) % 16777216
        secret_number = ((secret_number << 11) ^ secret_number) % 16777216
        yield secret_number


def main1() -> int:
    res = 0
    for number in parse_input(int):
        iterator = iterate(number)
        for _ in range(2001):
            number = next(iterator)
        res += number
    return res


def main2() -> int:
    prices_by_sequence = defaultdict(int)
    for number in parse_input(int):
        seen_sequences = set()
        iterator = iterate(number)
        collector = deque(maxlen=5)
        for _ in range(2001):
            number = next(iterator)
            collector.append(number % 10)
            if len(collector) == 5:
                a, b, c, d, e = collector
                sequence = (b - a, c - b, d - c, e - d)
                if sequence in seen_sequences:
                    continue
                seen_sequences.add(sequence)
                prices_by_sequence[sequence] += e
    return max(prices_by_sequence.values())
